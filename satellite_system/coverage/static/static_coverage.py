from typing import List, Set, Tuple
import numpy as np
import numpy.typing as npt
from datetime import *
from satellite_system.pos_prediction.pos_prediction import *
from satellite_system.groups.group import Group
from satellite_system.utils.constants import EARTH_RADIUS
from satellite_system.utils.hex_manager import HexManager
from satellite_system.utils.coord_converter import  *


class StaticCoverage:
    def __init__(self, group: Group, resolution: int):
        self.group = group
        self.resolution = resolution
        self.cache: dict[datetime, float] = {}
        self.aperture_angles: npt.NDArray[float] = None
        self.centers: List[Tuple[float, float]] = None

    def preprocess(self):
        centers_list = HexManager().get_centers(self.resolution)
        centers_list.sort(key = lambda x: x[0])
        self.centers = centers_list

        np_view = GroupNumpyView(self.group)
        view_angles_rad = np.radians(np_view.view_angles)

        self.aperture_angles = np.degrees(
            np.arcsin((1 + np_view.heights / EARTH_RADIUS) * np.sin(
                view_angles_rad))) - np_view.view_angles

    def get_covered_centers_union(self, target_time: datetime) -> List[Tuple[float, float]]:
        if self.centers is None:
            self.preprocess()

        result = np.empty(0, dtype=CenterCoord_dtype)

        predictor = PosPrediction(self.group)
        positions = predictor.predict_positions(target_time)

        min_lats = np.clip(positions[LAT] - self.aperture_angles, -90, 90)
        max_lats = np.clip(positions[LAT] + self.aperture_angles, -90, 90)
        if (min_lats == -90 or max_lats == 90):
            lon_mask = True
        else:
            min_lons = (positions[LON] - self.aperture_angles) % 360
            max_lons = (positions[LON] + self.aperture_angles) % 360

        for i in range(len(positions)):
            lat_min = min_lats[i]
            lat_max = max_lats[i]
            lon_min = min_lons[i]
            lon_max = max_lons[i]
            lower_bound = np.searchsorted(self.centers[LAT], lat_min, side="left")
            upper_bound = np.searchsorted(self.centers[LAT], lat_max, side="right")
            candidate_points = self.centers[lower_bound:upper_bound]

            center_lons = candidate_points[LON]
            if lon_min <= lon_max:
                lon_mask = (center_lons >= lon_min) & (center_lons <= lon_max)
            else:
                lon_mask = (center_lons >= lon_min) | (center_lons <= lon_max)
            candidate_points = candidate_points[lon_mask]

            sat_structured_np = CoordConverter().geo_to_dec_single(positions[LAT][i], positions[LON][i], positions["height"][i])
            sat_np = sat_structured_np.view((float, 3)).T

            candidates_structured_np = CoordConverter().geo_2d_to_dec_np(candidate_points)
            candidates_np = candidates_structured_np.view((float, 3))
            cos_center = (candidates_np @ sat_np) / np.linalg.norm(candidates_np, axis=1, keepdims=True) / np.linalg.norm(sat_np)
            cos_aperture_angle = np.cos(np.radians(self.aperture_angles[i]))
            final_mask = (cos_aperture_angle <= cos_center).ravel()
            result = np.concatenate((result, candidate_points[final_mask]))

        return np.unique(result)

    def calculate_coverage(self, target_time: datetime) -> float:
        if target_time in self.cache:
            return self.cache[target_time]
        return len(self.get_covered_centers_union(target_time)) / HexManager().get_total_number(self.resolution)
