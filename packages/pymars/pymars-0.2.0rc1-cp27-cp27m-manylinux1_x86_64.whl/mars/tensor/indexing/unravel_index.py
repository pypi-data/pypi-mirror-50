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

from collections import Iterable

import numpy as np

from ... import opcodes as OperandDef
from ...serialize import ValueType, KeyField, TupleField
from ...core import ExecutableTuple
from ..operands import TensorHasInput, TensorOperandMixin
from ..datasource import tensor as astensor
from ..array_utils import as_same_device, device
from ...compat import izip


class TensorUnravelIndex(TensorHasInput, TensorOperandMixin):
    _op_type_ = OperandDef.UNRAVEL_INDEX

    _input = KeyField('input')
    _dims = TupleField('dims', ValueType.int32)

    def __init__(self, dims=None, dtype=None, **kw):
        super(TensorUnravelIndex, self).__init__(_dims=dims, _dtype=dtype, **kw)

    @property
    def dims(self):
        return self._dims

    @property
    def output_limit(self):
        return float('inf')

    def _set_inputs(self, inputs):
        super(TensorUnravelIndex, self)._set_inputs(inputs)
        self._input = self._inputs[0]

    def __call__(self, indices):
        kws = [{'pos': i} for i in range(len(self._dims))]
        return ExecutableTuple(self.new_tensors([indices], indices.shape, kws=kws, output_limit=len(kws)))

    @classmethod
    def tile(cls, op):
        indices = op.inputs[0]
        dims = op.dims

        out_chunks = [list() for _ in range(len(dims))]
        for in_chunk in indices.chunks:
            chunk_op = op.copy().reset_key()
            chunk_kws = [{'pos': i, 'index': in_chunk.index} for i in range(len(dims))]
            chunks = chunk_op.new_chunks([in_chunk], shape=in_chunk.shape, kws=chunk_kws,
                                         output_limit=len(dims))
            for out_chunk, c in zip(out_chunks, chunks):
                out_chunk.append(c)

        new_op = op.copy()
        kws = [{'chunks': out_chunk, 'nsplits': indices.nsplits, 'shape': o.shape}
               for out_chunk, o in zip(out_chunks, op.outputs)]
        return new_op.new_tensors(op.inputs, kws=kws, output_limit=len(dims))

    @classmethod
    def execute(cls, ctx, op):
        inputs, device_id, xp = as_same_device(
            [ctx[c.key] for c in op.inputs], device=op.device, ret_extra=True)
        indices = inputs[0]

        with device(device_id):
            outputs = xp.unravel_index(indices, op.dims)
            for o, output in izip(op.outputs, outputs):
                ctx[o.key] = output


def unravel_index(indices, dims):
    """
    Converts a flat index or tensor of flat indices into a tuple
    of coordinate tensors.

    Parameters
    ----------
    indices : array_like
        An integer tensor whose elements are indices into the flattened
        version of a tensor of dimensions ``dims``.
    dims : tuple of ints
        The shape of the tensor to use for unraveling ``indices``.

    Returns
    -------
    unraveled_coords : tuple of Tensor
        Each tensor in the tuple has the same shape as the ``indices``
        tensor.

    See Also
    --------
    ravel_multi_index

    Examples
    --------
    >>> import mars.tensor as mt
    >>> from mars.session import new_session

    >>> sess = new_session().as_default()

    >>> sess.run(mt.unravel_index([22, 41, 37], (7,6)))
    (array([3, 6, 6]), array([4, 5, 1]))

    >>> sess.run(mt.unravel_index(1621, (6,7,8,9)))
    (3, 1, 4, 1)
    """
    indices = astensor(indices)
    if isinstance(dims, Iterable):
        dims = tuple(dims)
    else:
        dims = (dims,)

    op = TensorUnravelIndex(dims=dims, dtype=np.dtype(np.intp))
    return op(indices)
