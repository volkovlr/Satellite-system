from __future__ import annotations
import datetime
from typing import Dict, Any

class Satellite:
    def __init__(
        self,
        view_angle: float,
        phase: float,
        reg_number: int,
        group_number: int,
        launch_date: datetime.datetime,
        state: str
    ):
        """Satellite class

        Args:
            view_angle (float)
            phase (float)
            reg_number (int)
            group_number (int)
            launch_date (datetime.datetime)
            state (str)
        """
        self.view_angle = view_angle
        self.phase = phase
        self.reg_number = reg_number
        self.group_number = group_number
        self.launch_date = launch_date
        self.state = state

    @classmethod
    def from_gr_config(cls, group_config: Dict[str, Any], phase: float, number: int, group_number: int) -> Satellite:
        """A function for creating a Satellite from the configuration of the entire grouping

        Args:
            group_config (Dict[str, Any])
            phase (float)
            number (int)
            group_number (int)

        Returns:
            Satellite
        """
        return cls(group_config["view_angle"],
                   phase,
                   number,
                   group_number,
                   group_config["t0"],
                   "at work")
