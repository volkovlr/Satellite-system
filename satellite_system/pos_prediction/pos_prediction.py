import datetime
from ..groups.group import Group
from ..constants.constants import Constants
from ..coord_converter.coord_converter import CoordConverter

class PosPrediction:
    def init(
        self,
        group: Group,
        geom_info: Dict[int, GeoCoord]
    ):
        self.group = group
        self.geom_info = {}

    def predict_positions(self, target_time: datetime) -> Dict[int, Tuple(GeoCoord, float]):
        for orbit in self.group.orbits:
            new_longitude_asceding_node = (orbit.longitude_asceding_node - Constants.EarthAngularVelocityGrad * (target_time - orbit.creat_date) + 360) % 360
            for satellite in orbit.satellites:
                coord = CoordConverter.phase_to_geo(new_longitude_asceding_node, satellite.phase, orbit.height))
                self.geom_info[satellite.reg_number] = (coord, satellite.view_angle)