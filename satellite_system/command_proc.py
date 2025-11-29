from satellite_system.utils.singleton import singleton
from .coordinator import Coordinator

@singleton
class CommandProcessor:
    def __init__(self):
        self.coordinator = Coordinator()
        self.commands = {"add_group" : self.coordinator.add_group}

    def execute(self, input_line: str) -> str:
        parts = input_line.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd not in self.commands.keys():
            raise ValueError("Unknown command")

        return self.commands[cmd](args)
