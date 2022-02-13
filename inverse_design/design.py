# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/02_design.ipynb (unless otherwise specified).

__all__ = ['UNASSIGNED', 'VOID', 'SOLID', 'PIXEL_IMPOSSIBLE', 'PIXEL_EXISTING', 'PIXEL_POSSIBLE', 'PIXEL_REQUIRED',
           'TOUCH_REQUIRED', 'TOUCH_INVALID', 'TOUCH_EXISTING', 'TOUCH_VALID', 'TOUCH_FREE', 'TOUCH_RESOLVING',
           'Design', 'new_design', 'design_mask', 'visualize']

# Internal Cell
from typing import NamedTuple

import jax.numpy as jnp
import matplotlib.pyplot as plt
from fastcore.basics import patch_to
from matplotlib.colors import ListedColormap

# Cell
UNASSIGNED = 0
VOID = 1
SOLID = 2
PIXEL_IMPOSSIBLE = 3
PIXEL_EXISTING = 4
PIXEL_POSSIBLE = 5
PIXEL_REQUIRED = 6
TOUCH_REQUIRED = 7
TOUCH_INVALID = 8
TOUCH_EXISTING = 9
TOUCH_VALID = 10
TOUCH_FREE = 11
TOUCH_RESOLVING = 12

# Cell
class Design(NamedTuple):
    design: jnp.ndarray
    void_pixels: jnp.ndarray
    solid_pixels: jnp.ndarray
    void_touches: jnp.ndarray
    solid_touches: jnp.ndarray

    @property
    def shape(self):
        return self.design.shape

    def copy(self, **kwargs):
        kwargs = {name: kwargs.get(name, getattr(self, name)) for name in self._fields}
        return Design(*kwargs.values())

# Cell
def new_design(shape):
    return Design(
        design=jnp.zeros(shape, dtype=jnp.uint8).at[:,:].set(UNASSIGNED),
        void_pixels=jnp.zeros(shape, dtype=jnp.uint8).at[:,:].set(PIXEL_POSSIBLE),
        solid_pixels=jnp.zeros(shape, dtype=jnp.uint8).at[:,:].set(PIXEL_POSSIBLE),
        void_touches=jnp.zeros(shape, dtype=jnp.uint8).at[:,:].set(TOUCH_VALID),
        solid_touches=jnp.zeros(shape, dtype=jnp.uint8).at[:,:].set(TOUCH_VALID),
    )

# Cell
def design_mask(design, dtype=float):
    one = jnp.ones_like(design.design, dtype=dtype)
    mask = jnp.where(design.design == VOID, -1, one)
    return mask

# Cell
def visualize(design):
    _cmap = ListedColormap(colors={UNASSIGNED: "#929292", VOID: "#cbcbcb", SOLID: "#515151", PIXEL_IMPOSSIBLE: "#8dd3c7", PIXEL_EXISTING: "#ffffb3", PIXEL_POSSIBLE: "#bebada", PIXEL_REQUIRED: "#fb7f72", TOUCH_REQUIRED: "#00ff00", TOUCH_INVALID: "#7fb1d3", TOUCH_EXISTING: "#fdb462", TOUCH_VALID: "#b3de69", TOUCH_FREE: "#fccde5", TOUCH_RESOLVING: "#e0e0e0"}.values(), name="cmap")
    nx, ny = design.design.shape
    fig, axs = plt.subplots(1, 5, figsize=(15,3*nx/ny))
    for i, title in enumerate(design._fields):
        ax = axs[i]
        ax.set_title(title.replace("_", " "))
        ax.imshow(design[i], cmap=_cmap, vmin=UNASSIGNED, vmax=TOUCH_RESOLVING)
        ax.set_yticks(jnp.arange(nx)+0.5, ["" for i in range(nx)])
        ax.set_xticks(jnp.arange(ny)+0.5, ["" for i in range(ny)])
        ax.set_yticks(jnp.arange(nx), [f"{i}" for i in range(nx)], minor=True)
        ax.set_xticks(jnp.arange(ny), [f"{i}" for i in range(ny)], minor=True)
        ax.set_xlim(-0.5, ny-0.5)
        ax.set_ylim(nx-0.5, -0.5)
        ax.grid(visible=True, which="major", c="k")

@patch_to(Design)
def _repr_html_(self):
    visualize(self)
    return ""