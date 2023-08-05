from __future__ import division
import logging
import matplotlib.pyplot as plt
import ipywidgets as ipyw
import math
__all__ = ["volshow"]
__author__ = "Casper da Costa-Luis <casper.dcl@physics.org>"
__version__ = "0.0.0"

def volshow(vols, sharex=True, sharey=True, z=0, colorbar=True):
    """
    Jupyter notebook interactive volume display.

    @param vols  : [("title", 3darray), ...] or {"title": 3darray} or [3darray, ...].
      N.B.: `3darray` is `zyx`.
    @return: fig, axs
    """
    if isinstance(vols, dict):
        vols = vols.items()
    elif hasattr(vols, "shape") or hasattr(vols[0], "shape"):  # 4darray
        vols = [("", i) for i in vols]

    W = min(4, int(math.ceil(len(vols) ** 0.5)))
    H = int(math.ceil(len(vols) / W))
    assert W * H >= len(vols)
    fig = plt.figure()
    axs = [[None] * W for _ in range(H)]

    def plot_images(z=z):
        """z  : int, slice index"""
        plt.clf()

        axs[0][0] = plt.subplot(H, W, 1)
        plt.imshow(vols[0][1][z])
        if colorbar:
            plt.colorbar()

        for i, (title, vol) in enumerate(vols):
            if not i:
                continue
            axs[i // W][i % W] = plt.subplot(
                H, W, i + 1, sharex=axs[0][0] if sharex else None, sharey=axs[0][0] if sharey else None)
            plt.imshow(vol[z])
            plt.title(title)
            if colorbar:
                plt.colorbar()
        plt.show()

    ipyw.interact(plot_images,
        z=ipyw.IntSlider(min=0, max=len(vols[0][1]) - 1, step=1, value=len(vols[0][1])//2))
    return fig, axs
