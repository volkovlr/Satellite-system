from typing import List
from .group import Group
from .orbit import Orbit
from ..satellites.satellite import Satellite

class GroupBuilder:
    def build(self, group_config : Dict[str, float]) -> Group:
        
