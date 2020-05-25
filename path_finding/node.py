import math
from functools import total_ordering

# @total_ordering
class node:

    def __init__(self, parent, destination, position) -> None:
        self.parent = parent
        # self.destination = destination
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

        if self.parent is not None:
            self.g = self.parent.g + 1

            self.h = math.sqrt(
                pow((destination[1] - self.position[1]), 2) + pow((destination[0] - self.position[0]), 2))

            self.f = self.g + self.h

    def __eq__(self, other):
        return self.position == other.position

    # def __lt__(self, other):
    #     return self.f < other.f

    def __hash__(self):
        if self.parent is not None:
            return hash(hash(self.position) + hash(self.parent))

        return hash(self.position)
