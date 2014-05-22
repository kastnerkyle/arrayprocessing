"""Element types.

A list of antenna element types.

"""
import numpy as np

class BaseElement(object):

    """Base element.

    Should be inherited from by all elements.

    """

    def __init__(self):
        pass

    def _get_propagation(self, az, el):
        raise AssertionError('''This class is abstract.
                             Antenna elements should override this method!''')


class MonopoleElement(BaseElement):

    """Monopole element.

    Uniform response pattern over azimuth. One of the simplest element types.

    """

    def _get_propagation(self, az, el=np.pi / 2):
        propagation = np.zeros((3, 1), dtype='float32')
        propagation[0, :] = np.cos(az) * np.sin(el)
        propagation[1, :] = np.sin(az) * np.sin(el)
        propagation[2, :] = np.cos(el)
        return propagation
