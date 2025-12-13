from typing import List
import numpy as np
import numpy.typing as npt
from sats_numpy_view import SatsNumpyView
from orbits_numpy_view import OrbitsNumpyView
from ...groups.orbit import Orbit

class GroupNumpyView:
    """
    Immutable NumPy snapshot of a satellite group.
    """
    @staticmethod
    def _build_orbit_idx(orbits: List[Orbit]) -> npt.NDArray[np.int32]:
        orbit_idx = []
        for i, orbit in enumerate(orbits):
            for _ in orbit.satellites:
                orbit_idx.append(i)
        orbit_idx = np.array(orbit_idx, dtype=np.int32)
        return orbit_idx

    def __init__(self, orbits: List[Orbit]):
        self.orbits_view = OrbitsNumpyView(orbits)
        self.sats_view = SatsNumpyView(orbits)
        self.orbit_idx = GroupNumpyView._build_orbit_idx(orbits)
