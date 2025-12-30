from __future__ import annotations
import datetime
from satellite_system.satellites.satellite import Satellite
from typing import List, Dict, Optional, Any

class Orbit:
    def __init__(
        self,
        height: float,
        inclin: float,
        longitude_asc: float,

        creat_date: datetime.datetime,
        reg_number: int,
        satellites: Optional[List[Satellite]] = None
    ):
        """Orbit class

        Args:
            height (float)
            inclin (float)
            longitude_asc (float)
            creat_date (datetime.datetime)
            reg_number (int)
            satellites (Optional[List[Satellite]], optional)
        """
        self.height = height
        self.inclin = inclin
        self.longitude_asc = longitude_asc

        self.creat_date = creat_date
        self.reg_number = reg_number

        self.satellites: List[Satellite] = [] if satellites is None else satellites

    def add_satellite(self, sat: Satellite):
        """A function for adding a satellite

        Args:
            sat (Satellite)
        """
        self.satellites.append(sat)

    @classmethod
    def from_gr_config(cls, group_config: Dict[str, Any], longitude: float, number: int) -> Orbit:
        """A function for creating an orbit from the configuration of the entire grouping

        Args:
            group_config (Dict[str, Any])
            longitude (float)
            number (int)

        Returns:
            Orbit
        """
        return cls(group_config["height"],
                   group_config["orb_inclin"],
                   longitude,
                   group_config["t0"],
                   number)
