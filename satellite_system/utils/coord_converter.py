from .singleton import singleton
import numpy as np
import numpy.typing as npt
from satellite_system.utils.constants import EARTH_RADIUS

LAT = 0
LON = 1
HEIGHT = 2

ASC_LON = 0
INCLIN = 1
PHASE = 2
ORB_HEIGHT = 3

X = 0
Y = 1
Z = 2

@singleton
class CoordConverter:
    @staticmethod
    def phase_to_geo_np(phase_coord_np: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        longitude_asceding_nodes = phase_coord_np[ASC_LON]
        inclins = phase_coord_np[INCLIN]
        phases_on_orbit = phase_coord_np[PHASE]
        heights = phase_coord_np[ORB_HEIGHT]

        longitude_asceding_nodes_rad = np.radians(longitude_asceding_nodes)
        inclins_rad = np.radians(inclins)
        phases_on_orbit_rad = np.radians(phases_on_orbit)

        sin_lats = np.clip(
            np.sin(phases_on_orbit_rad) * np.sin(inclins_rad),
            -1.0, 1.0
        )

        lats_rad = np.arcsin(sin_lats)
        lats = np.degrees(lats_rad)

        def formula(longitude_asceding_nodes: np.ndarray, phases_on_orbit_rad: np.ndarray, inclins_rad: np.ndarray) -> np.ndarray:
            return (longitude_asceding_nodes + np.degrees(
                np.arctan2(
                    np.sin(phases_on_orbit_rad) * np.cos(inclins_rad),
                    np.cos(phases_on_orbit_rad)
                )
            )) % 360

        conditions = [phases_on_orbit == 90, inclins != 90, (0.5 * np.pi < phases_on_orbit_rad) & (phases_on_orbit_rad < 1.5 * np.pi), True]
        choices = [0, formula(longitude_asceding_nodes, phases_on_orbit_rad, inclins_rad), (longitude_asceding_nodes + 180) % 360, longitude_asceding_nodes]
        lons = np.select(conditions, choices)

        result = np.empty((3, lats.shape[0]), dtype=np.float64)
        result[LAT] = lats
        result[LON] = lons
        result[HEIGHT] = heights
        return result


    @staticmethod
    def geo_to_dec_np(geo_coord_np: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        lats = geo_coord_np[LAT]
        lons = geo_coord_np[LON]
        heights = geo_coord_np[HEIGHT]

        lats_rad = np.radians(lats)
        lons_rad = np.radians(lons)

        xs = (EARTH_RADIUS + heights) * np.cos(lats_rad) * np.cos(lons_rad)
        ys = (EARTH_RADIUS + heights) * np.cos(lats_rad) * np.sin(lons_rad)
        zs = (EARTH_RADIUS + heights) * np.sin(lats_rad)

        result = np.empty((3, lats.shape[0]), dtype=np.float64)
        result[X] = xs
        result[Y] = ys
        result[Z] = zs
        return result

    @staticmethod
    def geo_to_dec_single(lat: float, lon: float, height: float) -> npt.NDArray[np.float64]:
        geo_coord_np = np.array([[lat], [lon], [height]], dtype=np.float64)
        return CoordConverter().geo_to_dec_np(geo_coord_np)

    @staticmethod
    def geo_2d_to_dec_np(geo_2d_coord_np: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        geo_coord_np = np.empty((3, geo_2d_coord_np.shape[1]), dtype=np.float64)
        geo_coord_np[LAT] = geo_2d_coord_np[LAT]
        geo_coord_np[LON] = geo_2d_coord_np[LON]
        geo_coord_np[HEIGHT] = 0
        return CoordConverter().geo_to_dec_np(geo_coord_np)