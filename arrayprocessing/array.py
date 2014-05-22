"""Array definitions.

Contains arrays, beamforming, and null-steering.

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

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

        Expects a numpy array of any shape for az_arr
        If el_arr is specified, must be the same size as az_arr
        Returns a numpy array of

        """
        if el_arr is not None:
            assert az_arr.shape == el_arr.shape
        flat_az = az_arr.ravel()
        az_gains = np.zeros(flat_az.shape)
        for n, az in enumerate(flat_az):
            propagation = self._get_propagation(az)
            response = np.matrix(np.exp(-2j * np.pi * np.dot(
                self.geometry, propagation) * self.wavelength_spacing))
            az_gains[n] = np.abs(np.dot(self.beam_weights.H, response))[0, 0]
        return az_gains.reshape(az_arr.shape)

    def plot_gain(self, n_pts=50, min_az=-np.pi, max_az=np.pi, log_scale=True):
        """Plot the gain over azimuth for an array."""
        all_az = np.linspace(min_az, max_az, n_pts)
        all_gain = self.gain_response(all_az)
        if log_scale is True:
            all_gain = 10 * np.log(all_gain)
        plt.plot(all_az, all_gain, color='steelblue')
        plt.xlim(min_az, max_az)

    def plot_gain2D(self, n_pts=360, log_scale=True):
        """Plot the 2D gain pattern of an array."""
        x_plot_min = self.x_min - 1000
        x_plot_max = self.x_max + 1000
        y_plot_min = self.y_min - 1000
        y_plot_max = self.y_max + 1000

        # Based on tricontourf example from
        # http://matplotlib.org/examples/pylab_examples/tricontour_demo.html
        n_angles = n_pts
        n_radii = 10
        min_radius = 200
        radii = np.linspace(min_radius, y_plot_max, n_radii)

        angles = np.linspace(-np.pi, np.pi, n_angles, endpoint=False)
        angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)
        angles[:, 1::2] += np.pi / n_angles

        x = (radii * np.cos(angles)).ravel()
        y = (radii * np.sin(angles)).ravel()
        z = self.gain_response(angles).ravel()
        # Roll so that 0 degrees is north
        z = np.roll(z, z.shape[0] / 4)
        if log_scale:
            z = 10 * np.log(z)

        triang = tri.Triangulation(x, y)

        xmid = x[triang.triangles].mean(axis=1)
        ymid = y[triang.triangles].mean(axis=1)
        mask = np.where(xmid * xmid + ymid * ymid < min_radius * min_radius,
                        1, 0)
        triang.set_mask(mask)
        ax = plt.gca()
        ax.set_aspect('equal')
        alpha = .8
        plt.tricontourf(triang, z, cmap=plt.cm.Purples, alpha=alpha)
        plt.colorbar(alpha=alpha)
        self.plot_geometry()
        plt.xlim(x_plot_min, x_plot_max)
        plt.ylim(y_plot_min, y_plot_max)
        ax.patch.set_facecolor('white')
        ax.xaxis.set_major_locator(plt.NullLocator())
        ax.yaxis.set_major_locator(plt.NullLocator())
        plt.setp(ax.get_xticklabels(), visible=False)
        plt.setp(ax.get_yticklabels(), visible=False)


class UniformArrayMixin(BaseArrayMixin):

    """Equally weighted array."""

    def _get_beam_weights(self):
        return np.matrix([1.0] * self.n_ant).T


class ClassicalBeamformerMixin(BaseArrayMixin):

    """Classical beamforming."""

    def __init__(self, n_ant, beam_dir, geometry_type, wavelength_spacing=.5,
                 random_seed=None):
        self.beam_dir = beam_dir
        BaseArrayMixin.__init__(self, n_ant, geometry_type, wavelength_spacing,
                                random_seed)

    def _get_beam_weights(self):
        propagation = self._get_propagation(self.beam_dir)
        response = np.matrix(np.exp(-2j * np.pi * np.dot(
            self.geometry, propagation) * self.wavelength_spacing))
        return response / np.sqrt(np.dot(response.H, response))


class MonopoleArray(UniformArrayMixin, MonopoleElement):

    """Monopole array with no beamforming."""

    pass


class BeamformedMonopoleArray(ClassicalBeamformerMixin,
                              MonopoleElement):

    """Classically beamformed monopole array."""

    pass
