from typing import List
import numpy as np
import numpy.typing as npt
from sats_numpy_view import SatsNumpyView
from orbits_numpy_view import OrbitsNumpyView
from id_index import IdIndex
from ...groups.orbit import Orbit
from ...groups.group import Group

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

    def __init__(self, group: Group):
        self.orbits_view = OrbitsNumpyView(group.orbits)
        self.sats_view = SatsNumpyView(group.orbits)
        self.orbit_idx = GroupNumpyView._build_orbit_idx(group.orbits)
        self.id_index = IdIndex(orbit.reg_number for orbit in group.orbits)
