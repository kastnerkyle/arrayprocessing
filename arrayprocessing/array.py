"""Array definitions.

Contains arrays, beamforming, and null-steering.

"""

import numpy as np
import matplotlib.pyplot as plt

from .geometry import GeometryMixin
from .element import MonopoleElement


class BaseArrayMixin(GeometryMixin):

    """Core array functionality, including plots and shared calculations.

    This class should not be used directly! Inherit, and override
    _get_beam_weights instead.

    """

    def __init__(self, n_ant, geometry_type, wavelength_spacing=.5,
                 random_seed=None):
        self.n_ant = n_ant
        self.geometry_type = geometry_type
        GeometryMixin.__init__(self, n_ant, geometry_type, wavelength_spacing,
                               random_seed)
        self.wavelength_spacing = wavelength_spacing
        self.beam_weights = self._get_beam_weights()

    def _get_beam_weights(self):
        raise AssertionError("""Arrays should override this method!""")

    def gain_response(self, az_arr, el_arr=None):
        """Calculate gain responses for input azimuths.

        Returns a numpy array of length az_arr.shape[0]

        """
        az_gains = np.zeros(len(az_arr))
        for n, az in enumerate(az_arr):
            propagation = self._get_propagation(az)
            response = np.matrix(np.exp(-2j * np.pi * np.dot(
                self.geometry, propagation) * self.wavelength_spacing))
            az_gains[n] = np.abs(np.dot(self.beam_weights.H, response))[0, 0]
        return az_gains

    def _plot_beam_quadrant(self, quadrant, n_pts, x_plot_min, x_plot_max,
                            y_plot_min, y_plot_max):
        all_az = np.linspace(-np.pi, np.pi, n_pts)
        all_gain = self.gain_response(all_az)
        az_spacing = all_az[1] - all_az[0]
        if quadrant in [1, 3]:
            xs = np.linspace(x_plot_min, self.x_center, n_pts)
        elif quadrant in [2, 4]:
            xs = np.linspace(self.x_center, x_plot_max, n_pts)
        else:
            raise ValueError("Quadrant must be 1, 2, 3 or 4")

        for az in all_az:
            y1s = xs * np.tan(az - .5 * az_spacing)
            y2s = xs * np.tan(az + .5 * az_spacing)
            if quadrant in [1, 2]:
                plt.fill_between(xs, y1=y1s, y2=y2s, where=(
                    y1s >= -.5 * az_spacing) & (y2s >= -.5 * az_spacing))
            elif quadrant in [3, 4]:
                plt.fill_between(xs, y1=y1s, y2=y2s, where=(
                    y1s <= .5 * az_spacing) & (y2s <= .5 * az_spacing))

    def plot_beam(self, n_pts=50):
        """Plot the beam pattern of an array."""
        self.plot_geometry()
        x_plot_min = self.x_min - 1000
        x_plot_max = self.x_max + 1000
        y_plot_min = self.y_min - 1000
        y_plot_max = self.y_max + 1000
        plt.xlim(x_plot_min, x_plot_max)
        plt.ylim(y_plot_min, y_plot_max)
        for i in [1, 2, 3, 4]:
            self._plot_beam_quadrant(
                i, n_pts, x_plot_min, x_plot_max, y_plot_min, y_plot_max)
            break

    def plot_gain(self, n_pts=50, min_az=-np.pi, max_az=np.pi, log_scale=True):
        """Plot the gain over azimuth for an array."""
        all_gain = self.gain_response(np.linspace(min_az, max_az, n_pts))
        if log_scale is True:
            all_gain = 10 * np.log(all_gain)
        plt.plot(all_gain, color='steelblue')


class UniformArrayMixin(BaseArrayMixin):

    """Equally weighted array."""

    def _get_beam_weights(self):
        return np.matrix([1.0] * self.n_ant).T


class ClassicalBeamformerMixin(BaseArrayMixin):

    """Classical beamforming."""

    def __init__(self, n_ant, beam_dir, geometry_type='linear'):
        self.beam_dir = beam_dir
        BaseArrayMixin.__init__(self, n_ant, geometry_type)

    def _get_beam_weights(self):
        propagation = self._get_propagation(self.beam_dir)
        response = np.matrix(np.exp(-2j * np.pi * np.dot(
            self.geometry, propagation) * self.wavelength_spacing))
        return response / np.sqrt(np.dot(response.H, response))


class BeamformedMonopoleArray(ClassicalBeamformerMixin,
                              MonopoleElement):

    """Classically beamformed monopole array."""

    pass
