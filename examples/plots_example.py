"""A plotting example for arrayprocessing.

Arrays come with a few built-in plot types.

"""
import numpy as np
import matplotlib.pyplot as plt
from arrayprocessing.array import BeamformedMonopoleArray

#Create beamformed array
arr = BeamformedMonopoleArray(4, np.pi / 4, 'linear')

#Plot element positions
arr.plot_geometry()
plt.figure()

#Show azimuth response
arr.plot_gain2D()
plt.figure()

#Plot gain values over azimuth
arr.plot_gain()
plt.show()
