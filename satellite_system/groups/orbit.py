import datetime
from ..satellites.satellite import Satellite


class Orbit:
    def __init__(
        self,
        eccentricity: float
        semi_major_axis: float
        inclination: float
        longitude_asceding_node: float
        arg_periapsis: float
        mean_anomaly: float

        satellites: Satellite[],
        creat_date: datetime.datetime,
        reg_number: int
    ):
        self.satellites = satellites
        self.creat_date = creat_date
        self.reg_number = reg_number
