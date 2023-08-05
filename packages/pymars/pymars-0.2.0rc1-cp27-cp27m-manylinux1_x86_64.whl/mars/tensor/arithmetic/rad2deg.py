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

import numpy as np

from ... import opcodes as OperandDef
from ..utils import infer_dtype
from .core import TensorUnaryOp
from .utils import arithmetic_operand


@arithmetic_operand(sparse_mode='unary')
class TensorRad2deg(TensorUnaryOp):
    _op_type_ = OperandDef.RAD2DEG
    _func_name = 'rad2deg'


@infer_dtype(np.rad2deg)
def rad2deg(x, out=None, where=None, **kwargs):
    """
    Convert angles from radians to degrees.

    Parameters
    ----------
    x : array_like
        Angle in radians.
    out : Tensor, None, or tuple of Tensor and None, optional
        A location into which the result is stored. If provided, it must have
        a shape that the inputs broadcast to. If not provided or `None`,
        a freshly-allocated tensor is returned. A tuple (possible only as a
        keyword argument) must have length equal to the number of outputs.
    where : array_like, optional
        Values of True indicate to calculate the ufunc at that position, values
        of False indicate to leave the value in the output alone.
    **kwargs

    Returns
    -------
    y : Tensor
        The corresponding angle in degrees.

    See Also
    --------
    deg2rad : Convert angles from degrees to radians.

    Notes
    -----
    rad2deg(x) is ``180 * x / pi``.

    Examples
    --------
    >>> import mars.tensor as mt

    >>> mt.rad2deg(mt.pi/2).execute()
    90.0
    """
    op = TensorRad2deg(**kwargs)
    return op(x, out=out, where=where)
