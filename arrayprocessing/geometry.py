"""Geometry types.

All geometry layouts for arrays.

"""

import numpy as np
import matplotlib.pyplot as plt


def _gen_linear_array(n_ant, wavelength_spacing):
            return wavelength_spacing * np.array(
                [[i, 0., 0.] for i in range(n_ant)])

def _gen_diagonal_array(n_ant, wavelength_spacing):
    return wavelength_spacing * np.array(
        [[i, i, 0.] for i in range(n_ant)])

class GeometryMixin(object):

    """Sets geometry for an array.

    Currently monolithic, but may be split into separate mixins soon.

    """

    def __init__(self, n_ant, geometry_type='linear', wavelength_spacing=.5,
                 random_seed=None):
        self.random_state = np.random.RandomState(random_seed)
        self.n_ant = n_ant
        self.wavelength_spacing = wavelength_spacing
        if geometry_type == 'linear':
            self.geometry = _gen_linear_array(self.n_ant,
                                              self.wavelength_spacing)
        elif geometry_type == 'diagonal':
            self.geometry = _gen_diagonal_array(self.n_ant,
                                                self.wavelength_spacing)
        elif geometry_type == 'random':
            self.geometry = self.random_state.rand(n_ant, 3)
        elif geometry_type == 'circular':
            raise ValueError('TODO')
        elif geometry_type == 'y':
            if (self.n_ant - 4) % 3 != 0:
                raise ValueError("""
                                 (n_ant - 4) % 3 must equal 0' for y geometry!
                                 """)
            n_ants_per_leg = self.n_ant // 3
            linear_portion = _gen_linear_array(n_ants_per_leg + 1, self.wavelength_spacing)
            neg_diag = _gen_diagonal_array(n_ants_per_leg + 1,
                                           self.wavelength_spacing)[1:, :]
            neg_diag *= np.array([1, -1, 0])
            pos_diag = _gen_diagonal_array(n_ants_per_leg + 1,
                                           self.wavelength_spacing)[1:, :]
            diags = linear_portion[-1, :] + np.vstack((neg_diag, pos_diag))
            self.geometry = np.vstack((linear_portion, diags))

        elif geometry_type == 'arbitrary':
            raise ValueError('TODO')
        else:
            raise ValueError('Geometry type not supported!')
        self.geometry_type = geometry_type
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
