from satellite_system.satellites.satellite import Satellite
from satellite_system.groups.group import Group
from satellite_system.groups.orbit import Orbit
from satellite_system.groups.group_builder import GroupBuilder
from .decorators import add_group_str, calculate_coverage_str
from satellite_system.utils.logger import Logger
import satellite_system.coverage.static.static_coverage as static_cov
from typing import Dict
import datetime

from satellite_system.utils.singleton import singleton

@singleton
class Coordinator:
  def __init__(self):
      """Launch certain function (create group or calculating coverage) depending on user's input
      """
      self.groups: Dict[str, Group] = {}
      self.orbits: Dict[str, Orbit] = {}
      self.satellites: Dict[str, Satellite] = {}
      self.cache: Dict[(int, int), static_cov.StaticCoverageCalculator] = {}
      self.logger = Logger()

  @add_group_str
  def add_group(self, group_config : Dict[str, float]):
      """Add a group to the model (using group builder)

      Args:
          group_config (Dict[str, float]): group configuration
      """
      group = GroupBuilder(self).build(group_config)
      self.groups[group.reg_number] = group

      self.logger.result(f"Added a group with a number: {group.reg_number}")

  def add_orbit(self, orbit: Orbit):
      """Add an orbit to the model

      Args:
          orbit (Orbit)
      """
      self.orbits[orbit.reg_number] = orbit

  def add_satellite(self, sat: Satellite):
      """Add a satellite to the model

      Args:
          sat (Satellite)
      """
      self.satellites[sat.reg_number] = sat

  @calculate_coverage_str
  def calculate_coverage(self, group_number: int, resolution: int, target_time: datetime):
      """Calculates coverage by group

      Args:
          group (Group)
          resolution (int)
      """
      group = self.groups[group_number]
      if (group.reg_number, resolution) in self.cache:
          calculator = self.cache[(group.reg_number, resolution)]
      else:
          calculator = static_cov.StaticCoverage(group, resolution)
          self.cache[(group.reg_number, resolution)] = calculator
      return calculator.calculate_coverage(target_time)