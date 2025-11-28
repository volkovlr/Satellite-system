from typing import List, Dict
from .group import Group
from .orbit import Orbit
from ..satellites.satellite import Satellite

from utils.singleton import singleton

@singleton
class GroupBuilder:
  def __init__(self, coordinator):
    self.coordinator = coordinator

  def build(self, group_config: Dict[str, any]) -> Group:  # height, orb_inclin, longitude_asc, count_orbits
                                                             # count_satellites, phase_shift, ph_first_sat
                                                             # t0, view_angle
    for i in range(group_config[count_orbits]):

      orbit = Orbit(group_config[height], 
					group_config[orb_inclin],
					group_config[longitude_asc],
					group_config[t0]
					)

