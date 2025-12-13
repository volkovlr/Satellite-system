import numpy as np
from typing import List
from ..groups.orbit import Orbit

class OrbitNumpyView:
    """
        Convertation: from orbits list to NumPy arrays of orbit's fields
    """
    def __init__(self, orbits: List[Orbit]):
        L = len(orbits)

        self.height = np.empty(L, dtype=np.float64)
        self.inclin = np.empty(L, dtype=np.float64)
        self.longitude_asc = np.empty(L, dtype=np.float64)
        self.reg_number = np.empty(L, dtype=np.int64)

        for i, orbit in enumerate(orbits):
            self.height[i] = orbit.height
            self.inclin[i] = orbit.inclin
            self.longitude_asc[i] = orbit.longitude_asc
            self.reg_number[i] = orbit.reg_number
