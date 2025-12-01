from .singleton import singleton
import numpy as np
import numpy.typing as npt
import .constants


GeoCoord_dtype = np.dtype([
    ("lat", float),
    ("lon", float),
    ("height", float),
])

PhaseCoord_dtype = np.dtype([
    ("longitude_asceding_node", float),
    ("inclin", float),
    ("phase_on_orbit", float),
    ("height", float),
])

DecartCoord_dtype = np.dtype([
    ("x", float),
    ("y", float),
    ("z", float)
])

@singleton
class CoordConverter:
    @staticmethod
    def phase_to_geo_np(phase_coord_np: npt.NDArray[PhaseCoord_dtype]) -> npt.NDArray[GeoCoord_dtype]:
        longitude_asceding_nodes = phase_coord_np["longitude_asceding_node"]
        inclins = phase_coord_np["inclin"]
        phases_on_orbit = phase_coord_np["phase_on_orbit"]
        heights = phase_coord_np["height"]

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

        conditions = [phases_on_orbit_rad == 90, inclins_rad != 90, (0.5 * np.pi < phases_on_orbit_rad) & (phases_on_orbit_rad < 1.5 * np.pi), True]
        choices = [0, formula(longitude_asceding_nodes_rad, phases_on_orbit_rad, inclins_rad), (longitude_asceding_nodes + 180) % 360, longitude_asceding_nodes]
        lons = np.select(conditions, choices)

        result = np.empty(len(lats), dtype=GeoCoord_dtype)
        result["lat"] = lats
        result["lon"] = lons
        result["height"] = heights
        return result


    @staticmethod
    def geo_to_dec_np(geo_coord_np: npt.NDArray[GeoCoord_dtype]) -> npt.NDArray[DecartCoord_dtype]:
        lats = geo_coord_np["lat"]
        lons = geo_coord_np["lon"]
        heights = geo_coord_np["height"]

        lats_rad = np.radians(lats)
        lons_rad = np.radians(lons)

        xs = (сonstants.EARTH_RADIUS + heights) * np.cos(lats_rad) * np.cos(lons_rad)
        ys = (сonstants.EARTH_RADIUS + heights) * np.cos(lats_rad) * np.sin(lons_rad)
        zs = (сonstants.EARTH_RADIUS + heights) * np.sin(lats_rad)

        result = np.empty(len(lats), dtype=DecartCoord_dtype)
        result["x"] = xs
        result["y"] = ys
        result["z"] = zs

        return result
