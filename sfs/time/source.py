"""Compute the sound field generated by a sound source.

The Green's function describes the spatial sound propagation over time.

.. include:: math-definitions.rst

"""

from __future__ import division
import numpy as np
from scipy.interpolate import interp1d
from .. import util
from .. import defs


def point(xs, signal, t, grid, fs=None, c=None, interpolator_kind='linear'):
    r"""Source model for a point source: 3D Green's function.

    Calculates the scalar sound pressure field for a given point in
    time, evoked by source excitation signal.

    Parameters
    ----------
    xs : (3,) array_like
        Position of source in cartesian coordinates.
    signal : (N,) array_like
        Excitation signal.
    t : float
        Observed point in time.
    grid : triple of array_like
        The grid that is used for the sound field calculations.
        See `sfs.util.xyz_grid()`.
    fs: int, optional
        Sampling frequency in Hertz.
    c : float, optional
        Speed of sound.

    Returns
    -------
    numpy.ndarray
        Scalar sound pressure field, evaluated at positions given by
        *grid*.

    Notes
    -----
    .. math::

        g(x-x_s,t) = \frac{1}{4 \pi |x - x_s|} \dirac{t - \frac{|x -
        x_s|}{c}}

    """
    xs = util.asarray_1d(xs)
    signal = util.asarray_1d(signal)
    grid = util.as_xyz_components(grid)
    if fs is None:
        fs = defs.fs
    if c is None:
        c = defs.c
    r = np.linalg.norm(grid - xs)
    # evaluate g over grid
    g_amplitude = 1 / (4 * np.pi * r)
    g_time = r / c

    interpolator = interp1d(np.arange(len(signal)), signal,
                            kind=interpolator_kind, bounds_error=False,
                            fill_value=0)

    p = interpolator((t - g_time) * fs)

    return p * g_amplitude
