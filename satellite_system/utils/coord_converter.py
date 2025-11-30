from .singleton import singleton
from dataclasses import dataclass
import math


@dataclass
class GeoCoord:
    lat: float
    lon: float
    height: float


@dataclass
class PhaseCoord:
    longitude_asceding_node: float
    inclin: float
    phase_on_orbit: float
    height: float


@singleton
class CoordConverter:
    def phase_to_geo(self, phase_coord: PhaseCoord) -> GeoCoord:
        longitude_asceding_node, inclin, phase_on_orbit, height = phase_coord
        inclin_rad = math.radians(inclin)
        phase_on_orbit_rad = math.radians(phase_on_orbit)

        sin_lat = max(-1.0, min(1.0, math.sin(phase_on_orbit_rad) * math.sin(inclin_rad)))
        lat_rad = math.asin(sin_lat)
        lat = math.degrees(lat_rad)

        if inclin != 90:
            lon = (longitude_asceding_node + math.degrees(math.atan2(
                math.sin(phase_on_orbit_rad) * math.cos(inclin_rad),
                math.cos(phase_on_orbit_rad)
            ))) % 360
        else:
            lon = longitude_asceding_node

        return GeoCoord(lat, lon, height)