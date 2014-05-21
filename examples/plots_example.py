import numpy as np
import matplotlib.pyplot as plt
from arrayprocessing.array import BeamformedMonopoleArray

#Create beamformed array
arr = BeamformedMonopoleArray(4, np.pi / 4)
arr.plot_geometry()
plt.figure()
arr.plot_beam()
plt.figure()
arr.plot_gain()
