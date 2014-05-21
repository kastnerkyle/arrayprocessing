"""Geometry types.

All geometry layouts for arrays.

"""

import numpy as np
import matplotlib.pyplot as plt


class GeometryMixin(object):

    """Sets geometry for an array.

    Currently monolithic, but may be split into separate mixins soon.

    """

    def __init__(self, n_ant, geometry_type='linear', wavelength_spacing=.5,
                 random_seed=None):
        self.random_state = np.random.RandomState(random_seed)
        if geometry_type == 'linear':
            self.geometry = np.array([[i, 0., 0.] for i in range(
                n_ant)])
        elif geometry_type == 'random':
            self.geometry = self.random_state.rand(n_ant, 3)
        else:
            raise ValueError('Geometry type not supported!')
        self.geometry_type = geometry_type
        self.wavelength_spacing = wavelength_spacing
        self.x_coords = self.geometry[:, 0]
        self.y_coords = self.geometry[:, 1]
        self.x_center, self.x_min, self.x_max = self._center_min_max(
            self.x_coords)
        self.y_center, self.y_min, self.y_max = self._center_min_max(
            self.y_coords)

    def _center_min_max(self, coords):
        return np.mean(coords), np.min(coords), np.max(coords)

    def plot_geometry(self):
        """Plot array geometry."""
        plt.plot(self.x_coords, self.y_coords, 'o', color='steelblue')
        plt.xlim(self.x_min - 1, self.x_max + 1)
        plt.ylim(self.y_min - 1, self.y_max + 1)
