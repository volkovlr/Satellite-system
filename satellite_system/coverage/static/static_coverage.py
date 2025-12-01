from typing import List, Set, Tuple
from ..pos_prediction.pos_prediction import PosPrediction
from ..groups.group import Group
from dataclasses import dataclass
from ..utils.hex_manager import HexManager
import numpy as np
import math
import ..coord_converter
import ..utils.constants

@dataclass
class Aperture:
    center: GeoCoord
    aperture_angle: float


    def contains(self, point: GeoCoord) -> bool:
        x_point, y_point, z_point = CoordConverter().geo_to_decart(point)
        x_center, y_center, z_center = CoordConverter().geo_to_decart(center)
        point_vec = np.array([x_point, y_point, z_point])
        center_vec = np.array([x_center, y_center, z_center])
        return math.acos(np.dot(point_vec, center_vec) / (np.linalg.norm(center_vec) * np.linalg.norm(point_vec))) <= self.aperture_angle

    @staticmethod
    def calculate_aperture_angles_bulk(heights, view_angles):
        view_angles_rad = np.radians(view_angles)
        return 180 - view_angles_rad - np.degrees(
            np.arcsin((1 + heights / Constants.EARTH_RADIUS) * np.sin(view_angles_rad))
        )

class StaticCoverage:
    def init(
        self,
        group: Group,
        target_time: datetime
        covered_centers: Set[Tuple[float, float]]
    ):
        self.group = group
        self.target_time = target_time
        self.covered_centers = None



def get_covered_centers(self, coord: GeoCoord, view_angle: float]) -> set(Tuple[float, float]):
    if (self.covered_centers != None):
        return self.covered_centers

    view_angles = np.array([])
    for orbit in self.group.orbits:
        cur_view_angles = np.array([sat.view_angle for sat in orbit])
        view_angles.concatenate(view_angles, cur_view_angles)
    view_angles_rad = np.radians(view_angles)


    apreture_angles = 180 - view_angles_rad - np.degrees(
            np.arcsin((1 + heights / Constants.EARTH_RADIUS) * np.sin(view_angles_rad))
        )
def get_covered_centers_union(self):-> set(Tuple[float, float])

    for sat_reg_number, position in positions:
        covered_centers = get_covered_centers(position)
        covered_centers_union.update(covered_centers)

def calculate_coverage(self, target_time: datetime) -> float:
    return len(get_covered_centers_union(self, target_time)) / HexManager().get_total_number()
