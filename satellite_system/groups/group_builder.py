from typing import Dict, Any
from .group import Group
from .orbit import Orbit
from ..satellites.satellite import Satellite
from utils.random import RandomID
from ..coordinator import Coordinator
from utils.singleton import singleton

@singleton
class GroupBuilder:
    def __init__(self, coordinator: Coordinator):
        self.coordinator = coordinator
        self.random = RandomID()

    def build(self, group_config: Dict[str, Any]) -> Group:

        group = Group(group_config["t0"], self.random.get("group"))

        satel_per_orbit = group_config["count_satellites"] / group_config["count_orbits"]

        for i in range(group_config["count_orbits"]):
            longitude = (group_config["longitude_asc"] + i * (360 / group_config["count_orbits"])) % 360

            orbit = Orbit.from_gr_config(group_config, longitude, self.random.get("orbit"))

            group.add_orbit(orbit)
            self.coordinator.add_orbit(orbit)

            for k in range(satel_per_orbit):
                phase = (group_config["ph_first_sat"] +
                         k * (360 / satel_per_orbit) +
                         group_config["phase_shift"] * i) % 360

                satellite = Satellite.from_gr_config(group_config,
                                                     phase,
                                                     self.random.get("satellite"),
                                                     group.reg_number)

                orbit.add_satellite(satellite)
                self.coordinator.add_satellite(satellite)

        return group
