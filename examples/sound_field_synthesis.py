"""
    Illustrates the usage of the SFS toolbox for the simulation of SFS.

    This script contains almost all possibilities than can be used
    for the synthesis of sound fields generated by Wave Field Synthesis or
    Higher-Order Ambisonics with various loudspeaker configurations.
"""

import numpy as np
import matplotlib.pyplot as plt
import sfs


# simulation parameters
dx = 0.1  # secondary source distance
N = 64  # number of secondary sources
pw_angle = 0  # traveling direction of plane wave
xs = [2, 1, 0]  # position of virtual source
f = 500  # frequency
R = 1.5  # radius of spherical/circular array
x = np.arange(-2, 2, 0.02)  # spatial grid along x-axis
y = np.arange(-2, 2, 0.02)  # spatial grid along y-axis
grid = np.meshgrid(x, y, 0, sparse=True)

# angular frequency
omega = 2 * np.pi * f
# normal vector of plane wave
npw = sfs.util.normal(np.radians(pw_angle), np.radians(90))


# === get secondary source positions ===
#x0, n0, a0 = sfs.array.linear(N, dx)
#x0, n0, a0 = sfs.array.linear_nested(N, dx, 2*dx)
#x0, n0, a0 = sfs.array.linear_random(N, 0.2*dx, 5*dx)
#x0, n0, a0 = sfs.array.rectangular(2*N, dx, N, dx, n0=sfs.util.normal(0*np.pi/4, np.pi/2))
x0, n0, a0 = sfs.array.circular(N, R)

#x0, n0, a0 = sfs.array.planar(N, dx, N, dx, n0=sfs.util.normal(np.radians(0),np.radians(180)))
#x0, n0, a0 = sfs.array.cube(N, dx, N, dx, N, dx, n0=sfs.util.normal(0, np.pi/2))

#x0, n0, a0 = sfs.array.sphere_load('/Users/spors/Documents/src/SFS/data/spherical_grids/equally_spaced_points/006561points.mat', 1, center=[.5,0,0])


# === compute driving function ===
#d = sfs.mono.drivingfunction.delay_3d_plane(omega, x0, n0, npw)

#d = sfs.mono.drivingfunction.wfs_2d_line(omega, x0, n0, xs)

#d = sfs.mono.drivingfunction.wfs_2d_plane(omega, x0, n0, npw)
d = sfs.mono.drivingfunction.wfs_25d_plane(omega, x0, n0, npw)
#d = sfs.mono.drivingfunction.wfs_3d_plane(omega, x0, n0, npw)

#d = sfs.mono.drivingfunction.wfs_2d_point(omega, x0, n0, xs)
#d = sfs.mono.drivingfunction.wfs_25d_point(omega, x0, n0, xs)
#d = sfs.mono.drivingfunction.wfs_3d_point(omega, x0, n0, xs)

#d = sfs.mono.drivingfunction.nfchoa_2d_plane(omega, x0, R, npw)

#d = sfs.mono.drivingfunction.nfchoa_25d_point(omega, x0, R, xs)
#d = sfs.mono.drivingfunction.nfchoa_25d_plane(omega, x0, R, npw)

# === determine active secondary sources ===
a = sfs.mono.drivingfunction.source_selection_plane(n0, npw)
#a = sfs.mono.drivingfunction.source_selection_point(n0, x0, xs)
#a = sfs.mono.drivingfunction.source_selection_all(len(x0))


# === compute tapering window ===
twin = sfs.tapering.none(a)
#twin = sfs.tapering.kaiser(a)
#twin = sfs.tapering.tukey(a,.3)


# === compute synthesized sound field ===
p = sfs.mono.synthesized.generic(omega, x0, d * twin * a0 , grid,
                                 source=sfs.mono.source.point)


# === plot synthesized sound field ===
plt.figure(figsize=(10, 10))
sfs.plot.soundfield(p, grid, [0, 0, 0])
sfs.plot.loudspeaker_2d(x0, n0, twin)
plt.grid()
plt.savefig('soundfield.png')


#sfs.plot.loudspeaker_3d(x0, n0, twin)
#plt.savefig('loudspeakers.png')
