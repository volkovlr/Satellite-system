import numpy as np
from typing import List
from ...groups.orbit import Orbit

class SatsNumpyView:
    """
        Convertation: from orbits list to NumPy arrays of satellites' fields
    """
    def __init__(self, orbits: List[Orbit]):
        view_angle = []
        phase = []
        reg_number = []

        for i, orbit in enumerate(orbits):
            for sat in orbit.satellites:
                view_angle.append(sat.view_angle)
                phase.append(sat.phase)
                reg_number.append(sat.reg_number)

        self.view_angle = np.array(view_angle)
        self.phase = np.array(phase)
        self.reg_number = np.array(reg_number)
