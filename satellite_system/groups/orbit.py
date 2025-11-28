import datetime
from ..satellites.satellite import Satellite
from typing import List, Optional

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
        self.height = height
        self.inclin = inclin
        self.longitude_asc = longitude_asc

        self.creat_date = creat_date
        self.reg_number = reg_number

        self.satellites: List[Satellite] = [] if satellites is None else satellites

    def add_satellite(self, sat: Satellite):
        self.satellites.append(sat)
