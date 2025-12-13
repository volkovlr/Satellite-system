from typing import List
import numpy as np
from sats_numpy_view import SatsNumpyView
from orbits_numpy_view import OrbitsNumpyView
from ...groups.orbit import Orbit

class ExtendedSatsNumpyView:
    """
    Converts data of a group to numpy arrays
    """

    def __init__(self, orbits: List[Orbit]):
        orbits_view = OrbitsNumpyView(orbits)
        sats_view = SatsNumpyView(orbits)

        orbit_idx = []
        for i, orbit in enumerate(orbits):
            for _ in orbit.satellites:
                orbit_idx.append(i)
        orbit_idx = np.array(orbit_idx, dtype=np.int32)

        self.view_angle = sats_view.view_angle
        self.phase = sats_view.phase
        self.reg_number = sats_view.reg_number
        self.height = orbits_view.height[orbit_idx]
        self.inclin = orbits_view.inclin[orbit_idx]
        self.longitude_asc = orbits_view.longitude_asc[orbit_idx]
