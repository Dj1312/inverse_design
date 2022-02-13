# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/01_utils.ipynb (unless otherwise specified).

__all__ = ['conv2d', 'batch_conv2d', 'dilute', 'randn', 'rand', 'argmax2d', 'argmin2d']

# Internal Cell
from functools import wraps

import jax
import jax.numpy as jnp
import numpy as np
from jax.lax import conv

# Cell
@wraps(conv)
def conv2d(lhs, rhs, window_strides=(1,1), padding="SAME", **kwargs):
    return conv(lhs[None, None, :, :], rhs[None, None, :, :], window_strides, padding, **kwargs)[0, 0, :, :]

# Cell
@wraps(conv)
def batch_conv2d(lhs, rhs, window_strides=(1,1), padding="SAME", **kwargs):
    return conv(lhs[:, None, :, :], rhs[:, None, :, :], window_strides, padding, **kwargs)[:, 0, :, :]

# Cell
def dilute(touches, brush):
    return conv2d(
        lhs=touches,
        rhs=brush,
        window_strides=(1, 1),
        padding="SAME",
        preferred_element_type=bool,
    )

# Cell
def randn(shape, r=None, dtype=float):
    if r is not None:
        if isinstance(r, int):
            r = np.random.RandomState(seed=r)
    else:
        r = np.random
    return jnp.asarray(r.randn(*shape), dtype=dtype)

# Cell
def rand(shape, r=None, dtype=float):
    if r is not None:
        if isinstance(r, int):
            r = np.random.RandomState(seed=r)
    else:
        r = np.random
    return jnp.asarray(r.rand(*shape), dtype=dtype)

# Cell
@jax.jit
def argmax2d(arr2d):
    m, n = arr2d.shape
    arr1d = arr2d.ravel()
    k = jnp.argmax(arr1d)
    return k//m, k%m

# Cell
@jax.jit
def argmin2d(arr2d):
    m, n = arr2d.shape
    arr1d = arr2d.ravel()
    k = jnp.argmin(arr1d)
    return k//m, k%m