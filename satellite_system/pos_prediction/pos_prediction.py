from datetime import datetime
from ..groups.group import Group
from ..utils.constants import *
from satellite_system.utils.coord_converter import *
from ..groups.orbit import Orbit
from ..utils.numpy_views.group_numpy_view import GroupNumpyView

class PosPrediction:
    def __init__(self, group: Group):
        self.group = group
        self.cache = {}

    def predict_positions(self, target_time: datetime
                          ) -> dict[int, tuple[float, float, float]]:
        if target_time in self.cache:
            return self.cache[target_time]

        np_view = GroupNumpyView(self.group)
        time_delta = (target_time - np_view.orbit_view.creat_date).total_seconds()
        asc_lon_delta = - np.degrees(EARTH_ANGULAR_SPEED_RAD * time_delta)
        asc_lon_new = ((np_view.orbit_view.longitude_asc + asc_lon_delta) + 360) % 360
        sat_angular_speed_rad = np.sqrt((EARTH_MASS * G / (EARTH_RADIUS + np_view.orbit_view.height) ** 3))
        phase_delta = np.degrees(sat_angular_speed_rad * time_delta)

        phase_delta = phase_delta[np_view.orbit_idx]
        inclin = np_view.orbit_view.inclin[np_view.orbit_idx]
        height = np_view.orbit_view.height[np_view.orbit_idx]
        asc_lon_new = asc_lon_new[np_view.orbit_idx]

        phase_new = np_view.sats_view.phases + phase_delta

        phase_coords = np.empty((4, len(asc_lon_new)), dtype=np.float64)
        phase_coords[ASC_LON] = asc_lon_new
        phase_coords[INCLIN] = inclin
        phase_coords[PHASE] = phase_new
        phase_coords[HEIGHT] = height
        geo_coords = CoordConverter().phase_to_geo_np(phase_coords)

        result = (np_view.id_index.id(i) for i, coord in enumerate(geo_coords))
        self.cache[target_time] = result
        return result