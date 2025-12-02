from typing import List, Set, Tuple
import numpy as np
import numpy.typing as npt
import datetime
from ..pos_prediction.pos_prediction import PosPrediction
from ..groups.group import Group
from ..utils.hex_manager import HexManager
import ..utils.coord_converter
import ..utils.constants
from ..coord_converter.coord_converter import CoordConverter


CenterCoord_dtype = np.dtype([
    ("lat", float),
    ("lon", float),
])


class StaticCoverage:
    def __init__(self, group: Group, resolution: int):
        self.group = group
        self.resolution = resolution
        self.cache: dict[datetime, float] = {}
        self.aperture_angles: npt.NDArray[float] = None
        self.centers: npt.NDArray[CenterCoord_dtype] = None

    def preprocess(self):
        centers_list = HexManager().get_centers(self.resolution)
        self.centers = np.array(centers_list, dtype=CenterCoord_dtype)

        heights = np.array([orbit.height for orbit in self.group.orbits for _ in orbit.satellites])
        view_angles = np.array([satellite.view_angle for orbit in self.group.orbits for satellite in orbit.satellites])
        view_angles_rad = np.radians(view_angles)

        self.aperture_angles = 180 - view_angles - np.degrees(
            np.arcsin((1 + heights / constants.EARTH_RADIUS) * np.sin(
                view_angles_rad))
        )

    def get_covered_centers_union(self, target_time: datetime) -> npt.NDArray[CenterCoord_dtype]:
        if self.centers is None:
            self.preprocess()

        result = np.empty(0, dtype=CenterCoord_dtype)

        predictor = PosPrediction(self.group)
        positions = predictor.predict_positions(target_time)

        min_lats = np.clip(positions["lat"] - self.aperture_angles, -90, 90)
        max_lats = np.clip(positions["lat"] + self.aperture_angles, -90, 90)
        min_lons = (positions["lon"] - self.aperture_angles) % 360
        max_lons = (positions["lon"] + self.aperture_angles) % 360

        center_lats = self.centers["lat"]

        for i in range(len(positions)):
            lat_min = min_lats[i]
            lat_max = max_lats[i]
            lon_min = min_lons[i]
            lon_max = max_lons[i]

            lower_bound = np.searchsorted(center_lats, lat_min, side="left")
            upper_bound = np.searchsorted(center_lats, lat_max, side="right")
            candidate_points = self.centers[lower_bound:upper_bound]

            center_lons = candidate_points["lon"]
            if lon_min <= lon_max:
                lon_mask = (center_lons >= lon_min) & (center_lons <= lon_max)
            else:
                lon_mask = (center_lons >= lon_min) | (center_lons <= lon_max)
            candidate_points = candidate_points[lon_mask]

            sat_struct_dec = CoordConverter().geo_to_dec_single(positions["lat"][i], positions["lon"][i], positions["height"][i])
            sat_vec = np.array([sat_struct_dec["x"], sat_struct_dec["y"], sat_struct_dec["z"]])

            candidate_structs_dec = geo_to_dec_surface_np(candidate_points)
            candidate_vecs = np.vstack([candidate_structs_dec["x"], candidate_structs_dec["y"], candidate_structs_dec["z"]]).T

            cos_center = (candidate_vecs @ sat_vec) / np.linalg.norm(candidate_vecs, axis=1, keepdims=True) / np.linalg.norm(sat_vec)
            cos_aperture_angle = np.cos(np.radians(self.aperture_angles[i]))
            final_mask = (cos_aperture_angle >= cos_center)
            result = np.concatenate((result, candidate_points[final_mask]))

        return result

    def calculate_coverage(self, target_time: datetime) -> float:
        if target_time in self.cache:
            return self.cache[target_time]
        return len(self.get_covered_centers_union(target_time)) / HexManager().get_total_number(self.resolution)
