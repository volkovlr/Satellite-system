import datetime
from orbit import Orbit
from typing import List, Optional

class Group:
    def __init__(
        self,
        creat_date: datetime.datetime,
        reg_number: int,

        orbits: Optional[List[Orbit]] = None
    ):
        self.orbits = orbits
        self.creat_date = creat_date
        self.reg_number = reg_number

    def add_orbit(self, orbit: Orbit):
        self.orbits.append(orbit)
