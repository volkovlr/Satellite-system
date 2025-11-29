from satellites.satellite import Satellite
from groups.group import Group
from groups.orbit import Orbit
from groups.group_builder import GroupBuilder
from str_to_command import add_group_str
from utils.logger import Logger

from typing import Dict

from utils.singleton import singleton

@singleton
class Coordinator:
  def __init__(self):
      self.groups: Dict[str, Group] = {}
      self.orbits: Dict[str, Orbit] = {}
      self.satellites: Dict[str, Satellite] = {}

      self.logger = Logger()

  @add_group_str
  def add_group(self, group_config : Dict[str, float]):
      """
        Ключи в group_config:
        height, orb_inclin, longitude_asc, count_orbits,
        count_satellites, phase_shift, ph_first_sat,
        t0, view_angle
      """
      group = GroupBuilder(self).build(group_config)
      self.groups[group.reg_number] = group

      self.logger.result(f"Аdded a group with a number: {group.reg_number}")

  def add_orbit(self, orbit: Orbit):
      self.orbits[orbit.reg_number] = orbit

  def add_satellite(self, sat: Satellite):
      self.satellites[sat.reg_number] = sat
