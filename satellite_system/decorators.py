from __future__ import annotations
from typing import List
from satellite_system.config.constants import GROUP_PARAM_KEYS, CALCULATOR_PARAM_KEYS
import datetime

def add_group_str(func):
    """A decorator for possibility to accept a list of group configuration instead of dict

    Args:
        func (List)
    """
    def wrapper(self, line: List):
        """A function for convert list of group configuration to dict

        Args:
            line (List)

        Raises:
            ValueError
        """
        if len(line) != len(GROUP_PARAM_KEYS) + 1:
            raise ValueError("Uncorrect parameters")

        converted = []

        for i in range(len(line)):
            try:
                if i in [0, 1, 2, 5, 6, 9]:
                    converted.append(float(line[i]))

                elif i in [3, 4]:
                    converted.append(int(line[i]))

                elif i == 7:
                    date_str = line[i] + " " + line[i + 1]
                    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
                    converted.append(dt)

            except ValueError:
                raise ValueError("Uncorrect parameters")

        return func(self, dict(zip(GROUP_PARAM_KEYS, converted)))
    return wrapper


def calculate_coverage_str(func):
    """A decorator to convert calculator parameters from string

    Args:
        func (List)
    """
    def wrapper(self, line: List):
        """A function for convert string to calculator parameters

        Args:
            line (List)

        Raises:
            ValueError
        """
        if len(line) != len(CALCULATOR_PARAM_KEYS) + 1:
            raise ValueError("Uncorrect parameters")

        converted = []

        for i in range(len(line)):
            try:
                if i in [0, 1]:
                    converted.append(int(line[i]))

                elif i == 2:
                    date_str = line[i] + " " + line[i + 1]
                    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
                    converted.append(dt)

            except ValueError:
                raise ValueError("Uncorrect parameters")
        kwargs = dict(zip(CALCULATOR_PARAM_KEYS, converted))
        return func(self, **kwargs)
    return wrapper