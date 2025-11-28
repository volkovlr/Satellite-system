from typing import List, Dict, Any
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
        """
        Ключи в group_config:
        height, orb_inclin, longitude_asc, count_orbits,
        count_satellites, phase_shift, ph_first_sat,
        t0, view_angle
        """

        group = Group(group_config["t0"], self.random.get("group"))

        satel_per_orbit = group_config["count_satellites"] / group_config["count_orbits"]

        for i in range(group_config["count_orbits"]):
            longitude = (group_config["longitude_asc"] + i * (360 / group_config["count_orbits"])) % 360

            orbit = Orbit(
                group_config["height"],
                group_config["orb_inclin"],
                longitude,
                group_config["t0"],
                self.random.get("orbit"),
            )
            group.add_orbit(orbit)
            self.coordinator.add_orbit(orbit)

            for k in range(satel_per_orbit):
                phase = (group_config["ph_first_sat"] +
                         k * (360 / satel_per_orbit) +
                         group_config["phase_shift"] * i) % 360

                satellite = Satellite(
                    group_config["view_angle"],
                    phase,
                    self.random.get("satellite"),
                    group.reg_number,
                    group_config["t0"],
                    "at work"
                )
                orbit.add_satellite(satellite)
                self.coordinator.add_satellite(satellite)

        return group
