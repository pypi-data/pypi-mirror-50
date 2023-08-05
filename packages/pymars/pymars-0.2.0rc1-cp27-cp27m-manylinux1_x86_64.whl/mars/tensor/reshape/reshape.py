#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 1999-2018 Alibaba Group Holding Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import itertools

import numpy as np
from ..utils import decide_chunk_sizes
from ... import opcodes as OperandDef
from ...compat import six, izip
from ...serialize import KeyField, TupleField, ValueType
from ..datasource import tensor as astensor
from ..operands import TensorOperandMixin, TensorHasInput, TensorShuffleProxy, \
    TensorShuffleMap, TensorShuffleReduce
from ..array_utils import as_same_device, device
from ...utils import get_shuffle_input_keys_idxes

import logging

logger = logging.getLogger(__name__)


class TensorReshape(TensorHasInput, TensorOperandMixin):
    _op_type_ = OperandDef.RESHAPE

    _input = KeyField('input')
    _newshape = TupleField('newshape', ValueType.int64)

    def __init__(self, newshape=None, dtype=None, create_view=None, **kw):
        super(TensorReshape, self).__init__(_newshape=newshape, _dtype=dtype,
                                            _create_view=create_view, **kw)

    @property
    def newshape(self):
        return self._newshape

    def _set_inputs(self, inputs):
        super(TensorReshape, self)._set_inputs(inputs)
        self._input = self._inputs[0]

    def on_output_modify(self, new_output):
        return reshape(new_output, self._input.shape)

    def on_input_modify(self, new_input):
        op = self.copy().reset_key()
        return op(new_input)

    def __call__(self, a):
        return self.new_tensor([a], self._newshape)

    @staticmethod
    def _gen_reshape_rechunk_nsplits(old_shape, new_shape, nsplits):
        old_idx = len(old_shape) - 1
        new_idx = len(new_shape) - 1
        rechunk_nsplists = [None for _ in old_shape]
        reshape_nsplists = [None for _ in new_shape]

        while old_idx >= 0 or new_idx >= 0:
            old_dim_size = old_shape[old_idx]
            new_dim_size = new_shape[new_idx]

            if old_dim_size == new_dim_size:
                # nothing need to do
                rechunk_nsplists[old_idx] = nsplits[old_idx]
                reshape_nsplists[new_idx] = nsplits[old_idx]
                old_idx -= 1
                new_idx -= 1
                continue

            if old_dim_size == 1:
                rechunk_nsplists[old_idx] = (1,)
                old_idx -= 1
            elif new_dim_size == 1:
                reshape_nsplists[new_idx] = (1,)
                new_idx -= 1
            elif old_dim_size < new_dim_size:
                left_old_idx = old_idx - 1
                while left_old_idx >= 0 and \
                        np.prod(old_shape[left_old_idx: old_idx + 1]) < new_dim_size:
                    left_old_idx -= 1
                if np.prod(old_shape[left_old_idx: old_idx + 1]) != new_dim_size:
                    raise ValueError('shapes not compatible')

                for i in range(left_old_idx + 1, old_idx + 1):
                    # rechunk the higher dimension into 1 chunk
                    # e.g. ((2, 2, 2), [(3, 3), (4, 4))] -> [6, 8]
                    rechunk_nsplists[i] = (old_shape[i],)

                chunk_reduce = np.prod([len(c) for c in nsplits[left_old_idx + 1: old_idx + 1]])
                # cause the higher dimension has been concatenated,
                # the lowest dimension should be expanded to reduce size
                rechunk_nsplists[left_old_idx] = \
                    TensorReshape._expand_nsplit_by_reduce(nsplits[left_old_idx], chunk_reduce)

                size_reduce = np.prod(old_shape[left_old_idx + 1: old_idx + 1])
                reshape_nsplists[new_idx] = tuple(size_reduce * c for c in rechunk_nsplists[left_old_idx])

                old_idx = left_old_idx - 1
                new_idx -= 1
            else:
                assert old_dim_size > new_dim_size
                lef_new_idx = new_idx - 1
                while lef_new_idx >= 0 and \
                        np.prod(new_shape[lef_new_idx: new_idx + 1]) < old_dim_size:
                    lef_new_idx -= 1
                if np.prod(new_shape[lef_new_idx: new_idx + 1]) != old_dim_size:
                    raise ValueError('shapes not compatible')

                chunk_expand = np.prod(new_shape[lef_new_idx + 1: new_idx + 1])
                rechunk_nsplists[old_idx] = TensorReshape._reduce_nsplit_by_expand(nsplits[old_idx], chunk_expand)

                for i in range(lef_new_idx + 1, new_idx + 1):
                    reshape_nsplists[i] = (new_shape[i],)
                reshape_nsplists[lef_new_idx] = tuple(c // chunk_expand for c in rechunk_nsplists[old_idx])

                old_idx -= 1
                new_idx = lef_new_idx - 1

        assert np.prod([len(s) for s in rechunk_nsplists]) == \
               np.prod([len(s) for s in reshape_nsplists])
        return rechunk_nsplists, reshape_nsplists

    @staticmethod
    def _expand_nsplit_by_reduce(splits, reduced):
        if reduced == 1:
            return splits

        out = []
        for s in splits:
            x = s
            part = max(x / reduced, 1)
            while x >= 2 * part:
                out.append(int(part))
                x -= int(part)
            if x:
                out.append(x)
        assert sum(splits) == sum(out)
        return tuple(out)

    @staticmethod
    def _reduce_nsplit_by_expand(splits, expand):
        assert sum(splits) % expand == 0

        out = []
        residual = 0
        for chunk in splits:
            chunk += residual
            div = chunk // expand
            residual = chunk % expand
            good = expand * div
            if good:
                out.append(good)
        return tuple(out)

    @staticmethod
    def _tile_as_shuffle(op):
        in_tensor = op.input
        tensor = op.outputs[0]
        new_shape = op.newshape
        shuffle_inputs, shuffle_outputs = [], []
        axis_offsets = [[0] + np.cumsum(ns)[:-1].tolist() for ns in in_tensor.nsplits]

        max_chunk_size = max(max(tp) for tp in in_tensor.nsplits)
        out_nsplits = decide_chunk_sizes(new_shape, max_chunk_size, tensor.dtype.itemsize)
        chunk_size_idxes = (range(len(size)) for size in out_nsplits)

        for inp in in_tensor.chunks:
            offset = tuple(axis_offsets[axis][idx] for axis, idx in enumerate(inp.index))
            chunk_op = TensorReshapeMap(_input=inp, _axis_offsets=offset, _oldshape=in_tensor.shape,
                                        _newshape=new_shape, _new_chunk_size=(max_chunk_size,) * len(new_shape),
                                        _dtype=inp.dtype)
            shuffle_inputs.append(chunk_op.new_chunk([inp], shape=(np.nan,), index=inp.index))

        proxy_chunk = TensorShuffleProxy(dtype=in_tensor.dtype, _tensor_keys=[in_tensor.op.key]) \
            .new_chunk(shuffle_inputs, shape=())

        for chunk_shape, chunk_idx in izip(itertools.product(*out_nsplits),
                                           itertools.product(*chunk_size_idxes)):
            shuffle_key = ','.join(str(o) for o in chunk_idx)
            chunk_op = TensorReshapeReduce(_dtype=tensor.dtype, _shuffle_key=shuffle_key)
            shuffle_outputs.append(chunk_op.new_chunk([proxy_chunk], shape=chunk_shape, index=chunk_idx))

        new_op = op.copy()
        return new_op.new_tensors(op.inputs, new_shape, chunks=shuffle_outputs,
                                  nsplits=out_nsplits)

    @classmethod
    def tile(cls, op):
        in_tensor = op.input
        tensor = op.outputs[0]

        try:
            rechunk_nsplits, reshape_nsplits = cls._gen_reshape_rechunk_nsplits(
                in_tensor.shape, tensor.shape, in_tensor.nsplits)
            rechunked_tensor = in_tensor.rechunk(rechunk_nsplits).single_tiles()
            in_idxes = itertools.product(*[range(len(s)) for s in rechunk_nsplits])
            out_idxes = itertools.product(*[range(len(s)) for s in reshape_nsplits])
            out_shape = itertools.product(*[s for s in reshape_nsplits])
            out_chunks = []
            for input_idx, out_idx, out_shape in izip(in_idxes, out_idxes, out_shape):
                in_chunk = rechunked_tensor.cix[input_idx]
                chunk_op = op.copy().reset_key()
                chunk_op._newshape = out_shape
                out_chunk = chunk_op.new_chunk([in_chunk], shape=out_shape, index=out_idx)
                out_chunks.append(out_chunk)

            new_op = op.copy()
            return new_op.new_tensors(op.inputs, tensor.shape,
                                      chunks=out_chunks, nsplits=reshape_nsplits)
        except ValueError:
            # TODO: make this as default when shuffle is mature
            if getattr(op.extra_params, '_reshape_with_shuffle', False):
                return cls._tile_as_shuffle(op)

            # shape incompatible, we will first do flatten, then reshape to the new shape
            return [in_tensor.reshape(-1).single_tiles().reshape(tensor.shape).single_tiles()]

    @classmethod
    def execute(cls, ctx, op):
        (x,), device_id, xp = as_same_device(
            [ctx[c.key] for c in op.inputs], device=op.device, ret_extra=True)

        with device(device_id):
            ctx[op.outputs[0].key] = x.reshape(op.newshape)


class TensorReshapeMap(TensorShuffleMap, TensorOperandMixin):
    _op_type_ = OperandDef.RESHAPE_MAP

    _input = KeyField('input')
    _axis_offsets = TupleField('axis_offsets', ValueType.uint64)
    _oldshape = TupleField('oldshape', ValueType.uint64)
    _newshape = TupleField('newshape', ValueType.uint64)
    _new_chunk_size = TupleField('new_chunk_size', ValueType.uint64)

    def _set_inputs(self, inputs):
        super(TensorReshapeMap, self)._set_inputs(inputs)
        self._input = self._inputs[0]

    @property
    def axis_offsets(self):
        return self._axis_offsets

    @property
    def oldshape(self):
        return self._oldshape

    @property
    def newshape(self):
        return self._newshape

    @property
    def new_chunk_size(self):
        return self._new_chunk_size

    @classmethod
    def execute(cls, ctx, op):
        chunk = op.outputs[0]
        # todo this function is an experimental one making shuffle runnable.
        # try elevate performance when needed.
        old_shape = op.oldshape
        new_shape = op.newshape
        new_chunk_size = op.new_chunk_size
        axis_offset = op.axis_offsets

        logger.debug('Reshape mapper: Start mapping step for %s', chunk.key)

        data = ctx[op.inputs[0].key]
        indices = list(np.nonzero(data))
        nz_data = data[indices]

        for idx in range(len(old_shape)):
            indices[idx] = np.add(indices[idx], axis_offset[idx], out=indices[idx])
        rest_indices = indices[0]
        indices[0] = None
        for idx in range(1, len(old_shape)):
            rest_indices = np.multiply(rest_indices, old_shape[idx], out=rest_indices)
            rest_indices = np.add(rest_indices, indices[idx], out=rest_indices)
            indices[idx] = None
        del indices

        new_indices = []
        for dim_size in reversed(new_shape[1:]):
            new_index = rest_indices % dim_size
            new_indices.append(new_index)
            rest_indices = np.floor_divide(rest_indices, dim_size, out=rest_indices)
        new_indices.append(rest_indices)
        new_indices.reverse()
        del rest_indices

        logger.debug('Reshape mapper: remapping to new locations for %s', chunk.key)

        dim_chunk_counts = [int(np.ceil(dim_size * 1.0 / chunk_size))
                            for dim_size, chunk_size in zip(new_shape, new_chunk_size)]
        target = new_indices[0] // new_chunk_size[0]
        for new_index, chunk_size, dim_chunk_count in zip(new_indices[1:], new_chunk_size[1:], dim_chunk_counts[1:]):
            target = np.multiply(target, dim_chunk_count, out=target)
            target = np.add(target, new_index // chunk_size, out=target)

        for idx, chunk_size in enumerate(new_chunk_size):
            new_indices[idx] = np.mod(new_indices[idx], chunk_size, out=new_indices[idx])

        logger.debug('Reshape mapper: sorting for %s', chunk.key)

        sort_idx = np.argsort(target)
        target = target[sort_idx]
        nz_data = nz_data[sort_idx]
        for idx in range(len(new_indices)):
            new_indices[idx] = new_indices[idx][sort_idx]
        del sort_idx

        logger.debug('Reshape mapper: splitting for %s', chunk.key)

        for t in np.unique(target):
            data_slice = slice(np.searchsorted(target, t), np.searchsorted(target, t, 'right'))
            group_indices = tuple(new_indices[idx][data_slice] for idx in range(len(new_shape)))
            group_data = nz_data[data_slice]

            target_chunk_idx = [None] * len(dim_chunk_counts)
            for idx, dim_chunk_count in enumerate(reversed(dim_chunk_counts)):
                t, target_chunk_idx[idx] = divmod(t, dim_chunk_count)
            target_chunk_idx.reverse()
            group_key = ','.join(str(v) for v in target_chunk_idx)

            ctx[(chunk.key, group_key)] = group_indices + (group_data,)

    @classmethod
    def estimate_size(cls, ctx, op):
        chunk = op.outputs[0]
        inp_chunk = chunk.inputs[0]
        inp_size, inp_calc = ctx[inp_chunk.key]
        store_overhead = np.int64().itemsize * inp_chunk.ndim
        calc_overhead = np.int64().itemsize * (inp_chunk.ndim + 2)
        ctx[chunk.key] = (store_overhead + inp_size, calc_overhead + inp_calc)


class TensorReshapeReduce(TensorShuffleReduce, TensorOperandMixin):
    _op_type_ = OperandDef.RESHAPE_REDUCE

    _input = KeyField('input')

    def _set_inputs(self, inputs):
        super(TensorReshapeReduce, self)._set_inputs(inputs)
        self._input = self._inputs[0]

    @classmethod
    def execute(cls, ctx, op):
        chunk = op.outputs[0]
        try:
            result_array = ctx[chunk.key]
        except KeyError:
            result_array = np.zeros(chunk.shape, dtype=chunk.dtype)

        in_chunk = chunk.inputs[0]
        input_keys, _ = get_shuffle_input_keys_idxes(in_chunk)

        shuffle_key = chunk.op.shuffle_key
        for input_key in input_keys:
            key = (input_key, shuffle_key)
            if ctx.get(key) is not None:
                data_tuple = ctx[key]
                result_array[data_tuple[:-1]] = data_tuple[-1]
            else:
                ctx[key] = None
        ctx[chunk.key] = result_array

    @classmethod
    def estimate_size(cls, ctx, op):
        chunk = op.outputs[0]
        sum_size = 0
        for shuffle_input in chunk.inputs[0].inputs or ():
            key = (shuffle_input.key, chunk.op.shuffle_key)
            if ctx.get(key) is not None:
                sum_size += ctx[key][0]
            else:
                ctx[key] = None
        ctx[chunk.key] = (chunk.nbytes, max(sum_size, chunk.nbytes))


def calc_shape(size, newshape):
    if isinstance(newshape, six.integer_types):
        newshape = (newshape,)
    else:
        newshape = tuple(int(s) for s in newshape)

    known_shape = [s for s in newshape if s >= 0]
    missing_dim = len(newshape) - len(known_shape)
    if missing_dim > 1:
        raise ValueError('can only specify one unknown dimension')
    if missing_dim == 1:
        known_size = np.prod(known_shape)
        newshape = tuple(int(size / known_size) if s < 0 and known_size > 0 else s
                         for s in newshape)

    return newshape


def reshape(a, newshape):
    """
    Gives a new shape to a tensor without changing its data.

    Parameters
    ----------
    a : array_like
        Tensor to be reshaped.
    newshape : int or tuple of ints
        The new shape should be compatible with the original shape. If
        an integer, then the result will be a 1-D tensor of that length.
        One shape dimension can be -1. In this case, the value is
        inferred from the length of the tensor and remaining dimensions.

    Returns
    -------
    reshaped_array : Tensor
        This will be a new view object if possible; otherwise, it will
        be a copy.

    See Also
    --------
    Tensor.reshape : Equivalent method.

    Notes
    -----
    It is not always possible to change the shape of a tensor without
    copying the data. If you want an error to be raised when the data is copied,
    you should assign the new shape to the shape attribute of the array::

    >>> import mars.tensor as mt

    >>> a = mt.arange(6).reshape((3, 2))
    >>> a.execute()
    array([[0, 1],
           [2, 3],
           [4, 5]])

    You can think of reshaping as first raveling the tensor (using the given
    index order), then inserting the elements from the raveled tensor into the
    new tensor using the same kind of index ordering as was used for the
    raveling.

    >>> mt.reshape(a, (2, 3)).execute()
    array([[0, 1, 2],
           [3, 4, 5]])
    >>> mt.reshape(mt.ravel(a), (2, 3)).execute()
    array([[0, 1, 2],
           [3, 4, 5]])

    Examples
    --------
    >>> a = mt.array([[1,2,3], [4,5,6]])
    >>> mt.reshape(a, 6).execute()
    array([1, 2, 3, 4, 5, 6])

    >>> mt.reshape(a, (3,-1)).execute()       # the unspecified value is inferred to be 2
    array([[1, 2],
           [3, 4],
           [5, 6]])
    """
    a = astensor(a)
    if np.isnan(sum(a.shape)):
        raise ValueError('tensor shape is unknown, {0}'.format(a.shape))

    newshape = calc_shape(a.size, newshape)
    if a.size != np.prod(newshape):
        raise ValueError('cannot reshape array of size {0} into shape {1}'.format(a.size, newshape))

    if a.shape == newshape:
        # does not need to reshape
        return a

    op = TensorReshape(newshape, dtype=a.dtype, create_view=True)
    return op(a)
