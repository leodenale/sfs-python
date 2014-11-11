"""Computation of synthesized sound fields."""

import sfs
import numpy as np


def generic(omega, x0, d, x, y, z, c=None, source_type='point'):
    """Compute sound field for a generic driving function"""
    d = np.squeeze(np.asarray(d))
    if len(d) != len(x0):
        raise ValueError("length mismatch")
    p = 0
    for weight, position in zip(d, x0):
        p += weight * getattr(sfs.mono.source, source_type)(omega, position, x, y, z, c)
    return p