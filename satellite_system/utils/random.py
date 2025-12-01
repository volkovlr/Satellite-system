import random
from .singleton import singleton

class Pool:
    def __init__(self, a: int, b: int):
        """A class for storing potential numbres of satellites/orbits/groups

        Args:
            a (int)
            b (int)
        """
        self.pool = list(range(a, b))
        random.shuffle(self.pool)
        self.index = 0

    def get(self) -> int:
        """Return the next number of object (satellite/orbit/group)

        Raises:
            RuntimeError

        Returns:
            int
        """
        if self.index >= len(self.pool):
            raise RuntimeError("The numbers in the range are over")

        ind = self.pool[self.index]
        self.index += 1
        return ind

@singleton
class RandomID:
    def __init__(self):
        """A class for storing pools of numbers
        """
        self.pools = {
            "group" : Pool(1000, 3000),
            "orbit" : Pool(10000, 12000),
            "satellite" : Pool(100000, 120000),
        }

    def get(self, name: str) -> int:
        """Return the next object number of the type 'name'

        Args:
            name (str)

        Returns:
            int
        """
        return self.pools[name].get()

