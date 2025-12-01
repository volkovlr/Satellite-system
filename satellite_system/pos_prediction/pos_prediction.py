import datetime
from ..groups.group import Group
from ..constants.constants import Constants
from ..coord_converter.coord_converter import CoordConverter

@dataclass
class SatGeomData:
    geo_coord: GeoCoord
    view_angle: float


class PosPrediction:
    def init(
        self,
        group: Group,
        cache: Dict[datetime, Dict[int, SatGeomData]]
    ):
        self.group = group
        self.cache = {}

    def predict_positions(self, target_time: datetime) -> Dict[int, SatGeomData]:
        longitude_asceding_nodes = np.array([orbit.longitude_asceding_node for orbit in self.group.orbits])
        creat_dates = np.array([orbit.creat_date for orbit in self.group.orbits])
        new_longitude_asceding_nodes = (longitude_asceding_nodes - Constants.EarthAngularVelocityGrad * (target_time - creat_dates) + 360) % 360
            for satellite in orbit.satellites:
                coord = CoordConverter.phase_to_geo(new_longitude_asceding_node, satellite.phase, orbit.height))
                self.positions[satellite.reg_number] = (coord, satellite.view_angle)