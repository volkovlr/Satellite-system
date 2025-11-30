from typing import List, Set, Tuple
from ..pos_prediction.pos_prediction import PosPrediction
from ..groups.group import Group
from dataclasses import dataclass
from ..utils.hex_manager import HexManager


@dataclass
class Aperture:
    center: GeoCoord
    radius_km: float

    def contains(self, point: GeoCoord) -> bool:
        pass


class StaticCoverage:
    def init(
        self,
        group: Group,
        covered_centers : List[Tuple[float, float]]
    ):
        self.group = group

def get_aperture_angle(
    self,
    coord: GeoCoord,
    view_angle: float
    ) -> float:
    """Выдаёт угол раствора шарового сектора, что покрывается спутником."""
    pass

def get_covered_centers(self, coord: GeoCoord, view_angle: float]):-> set(Tuple[float, float])
    pass

def get_covered_centers_union(self, target_time: datetime):-> set(Tuple[float, float])
    predictor = PosPrediction(group)
    positions = predictor.predict_positions(target_time)
    for sat_reg_number, position in positions:
        covered_centers = get_covered_centers(position)
        covered_centers_union.update(covered_centers)

def calculate_coverage(self, target_time: datetime):-> float
    return len(get_covered_centers_union(self, target_time)) / HexManager().get_total_number()
