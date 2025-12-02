import datetime
import numpy as np
import numpy.typing as npt
import ..utils.coord_converter
from ..groups.group import Group
import ..utils.constants
from ..coord_converter.coord_converter import CoordConverter


SatGeomData_dtype = np.dtype([
    ("lat", float),
    ("lon", float),
    ("height", float),
    ("veiw_angle", float),
    ("reg_number", int),
])


class PosPrediction:
    def __init__(self, group: Group):
        self.group = group
        self.cache = {}

    def predict_positions(self, target_time: datetime
                          ) -> npt.NDArray[SatGeomData_dtype]:
        if target_time in self.cache:
            return self.cache[target_time]

        for orbit in self.group.orbits:
            phase_coords = np.empty(len(orbit.satellites),
                                    dtype=PhaseCoord_dtype)

            phase_coords["longitude_asceding_node"] = (
                orbit.longitude_asceding_node
                - np.degrees(constants.EARTH_ANGULAR_VELOCITY_RAD
                             * (target_time - orbit.creat_date))
                + 360
            ) % 360

            phase_coords["inclin"] = orbit.inclin
            phase_coords["phase_on_orbit"] = np.array(
                [satellite.phase_on_orbit for satellite in orbit.satellites]
            )
            phase_coords["height"] = np.array(
                [satellite.height for satellite in orbit.satellites]
            )

            geo_coords = CoordConverter().phase_to_geo(phase_coords)

            result = np.empty(len(geo_coords), dtype=SatGeomData_dtype)
            result["lat"] = geo_coords["lat"]
            result["lon"] = geo_coords["lon"]
            result["height"] = geo_coords["height"]
            result["veiw_angle"] = np.array(
                [satellite.veiw_angle for satellite in orbit.satellites]
            )
            result["reg_number"] = np.array(
                [satellite.reg_number for satellite in orbit.satellites]
            )

        self.cache[target_time] = result
        return result
