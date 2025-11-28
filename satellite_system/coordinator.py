from satellites.satellite import Satellite
from groups.group import Group
from groups.orbit import Orbit
from groups.group_builder import GroupBuilder

from typing import Dict

from utils.singleton import singleton

@singleton
class Coordinator:
  def __init__(self):
    self.groups = {}
    self.orbits = {}
    self.satellites = {}

  def add_group(self, group_config : Dict[str, float]):
    group = GroupBuilder.build(group_config, self)
    self.groups[group.id] = group
