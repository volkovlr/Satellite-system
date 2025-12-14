from typing import List, Tuple
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
        self.np_view = None

    def preprocess(self):
        centers_list = HexManager().get_centers(self.resolution)
        centers_list.sort(key = lambda x: x[0])
        self.centers = centers_list

        self.np_view = GroupNumpyView(self.group)
        view_angles_rad = np.radians(self.np_view.sats_view.view_angle)

        height = self.np_view.orbits_view.height[self.np_view.orbit_idx]
        self.aperture_angles = np.degrees(
            np.arcsin((1 + height / EARTH_RADIUS) * np.sin(
                view_angles_rad))) - self.np_view.sats_view.view_angle

    def cell_filter(self, positions: dict[int, tuple[float, float, float]]) -> List[List[Tuple[float, float]]]:
        positions_np = (np.asarray(list(positions.values()), dtype=np.float64).T)[:, self.np_view.orbit_idx]

        centers = np.asarray(self.centers, dtype=np.float64).T
        centers_lat = centers[LAT]
        centers_lon = centers[LON]

        min_lats = np.clip(positions_np[LAT] - self.aperture_angles, -90.0, 90.0)
        max_lats = np.clip(positions_np[LAT] + self.aperture_angles, -90.0, 90.0)

        lower_bound = np.searchsorted(centers_lat, min_lats, side="left")
        upper_bound = np.searchsorted(centers_lat, max_lats, side="right")

        polar_mask = (min_lats == -90.0) | (max_lats == 90.0)
        max_abs_lats = np.where(polar_mask, 0.0, np.maximum(np.abs(min_lats), np.abs(max_lats)))

        min_lons = (positions_np[LON] - self.aperture_angles / np.cos(np.radians(max_abs_lats))) % 360.0
        max_lons = (positions_np[LON] + self.aperture_angles / np.cos(np.radians(max_abs_lats))) % 360.0

        result = []

        for i in range(positions_np.shape[1]):
            lat_mask = np.zeros(centers.shape[1], dtype=bool)
            lat_mask[lower_bound[i]:upper_bound[i]] = True

            if polar_mask[i]:
                result.append(list(zip(centers[LAT, lat_mask], centers[LON, lat_mask])))
            else:
                if min_lons[i] <= max_lons[i]:
                    lon_mask = (centers_lon >= min_lons[i]) & (centers_lon <= max_lons[i])
                else:
                    lon_mask = (centers_lon >= min_lons[i]) | (centers_lon <= max_lons[i])

                mask = lat_mask & lon_mask
                result.append(list(zip(centers[LAT, mask], centers[LON, mask])))
        return result

    def get_covered_centers_union(self, target_time: datetime) -> List[Tuple[float, float]]:
        if self.centers is None:
            self.preprocess()

        predictor = PosPrediction(self.group)
        sat_positions = predictor.predict_positions(target_time)
        print (len(sat_positions))
        sat_coords_geo_np = np.asarray(list(sat_positions.values()), dtype=np.float64).T
        sat_coords_xyz_np = CoordConverter().geo_2d_to_dec_np(sat_coords_geo_np)

        total_candidates = self.cell_filter(sat_positions)
        result = []
        for i in range(len(total_candidates)):
            if len(total_candidates[i]) == 0:
                continue

            cur_candidates_np = np.asarray(total_candidates[i], dtype=np.float64).T
            cur_candidates_xyz_np = CoordConverter().geo_2d_to_dec_np(cur_candidates_np)
            cos_candidate = (
                    (cur_candidates_xyz_np.T @ sat_coords_xyz_np[:, i])
                    / np.linalg.norm(cur_candidates_xyz_np, axis=0)
                    / np.linalg.norm(sat_coords_xyz_np[:, i])
            )

            cos_aperture = np.cos(np.radians(self.aperture_angles[i]))

            angle_mask = (cos_candidate >= cos_aperture)
            print(angle_mask)
            result.extend(map(tuple, cur_candidates_np[:, angle_mask].T))

        return list(set(result))

    def calculate_coverage(self, target_time: datetime) -> float:
        if target_time in self.cache:
            return self.cache[target_time]
        return len(self.get_covered_centers_union(target_time)) / HexManager().get_total_number(self.resolution)
