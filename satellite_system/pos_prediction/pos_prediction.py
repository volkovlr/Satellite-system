from datetime import datetime
from ..groups.group import Group
from ..utils.constants import *
from satellite_system.utils.coord_converter import *
from ..groups.orbit import Orbit
from ..utils.numpy_views.group_numpy_view import GroupNumpyView

class PosPrediction:
    def __init__(self, group: Group):
        self.group = group
        self.np_view = GroupNumpyView(self.group)
        self.cache = {}

    def predict_positions(self, target_time: datetime
                          ) -> dict[int, tuple[float, float, float]]:
        target_time = np.datetime64(target_time, 'us')
        if target_time in self.cache:
            return self.cache[target_time]

        time_delta = (target_time - self.np_view.orbits_view.creat_date) / np.timedelta64(1, 's')
        asc_lon_delta = - np.degrees(EARTH_ANGULAR_SPEED_RAD * time_delta)
        asc_lon_new = ((self.np_view.orbits_view.longitude_asc + asc_lon_delta) + 360) % 360
        sat_angular_speed_rad = np.sqrt((EARTH_MASS * G / (EARTH_RADIUS + self.np_view.orbits_view.height) ** 3))
        phase_delta = np.degrees(sat_angular_speed_rad * time_delta)

        phase_delta = phase_delta[self.np_view.orbit_idx]
        inclin = self.np_view.orbits_view.inclin[self.np_view.orbit_idx]
        height = self.np_view.orbits_view.height[self.np_view.orbit_idx]
        asc_lon_new = asc_lon_new[self.np_view.orbit_idx]

        phase_new = self.np_view.sats_view.phase + phase_delta

        phase_coords = np.empty((4, len(asc_lon_new)), dtype=np.float64)
        phase_coords[ASC_LON] = asc_lon_new
        phase_coords[INCLIN] = inclin
        phase_coords[PHASE] = phase_new
        phase_coords[HEIGHT] = height
        geo_coords = CoordConverter().phase_to_geo_np(phase_coords)

        result = {
            self.np_view.id_index.id(i): tuple(geo_coords[:, i])
            for i in range(geo_coords.shape[1])
        }
        self.cache[target_time] = result
        return result
