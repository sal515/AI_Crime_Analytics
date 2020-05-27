from path_finding.node import node
import math


class vertex:

    def __init__(self, node_a: node, node_b: node, parent, destination: node) -> None:
        self.parent = parent
        self.destination = destination

        self.node_a = node_a
        self.node_b = node_b

        self.g = 0
        self.h = 0
        self.f = 0

        if self.parent is not None:
            # FIXME
            self.g = self.parent.g + 1

            self.h = math.sqrt(
                pow((self.destination.y - self.node_b.y), 2) + pow(
                    (self.destination.x - self.node_b.x), 2))

            self.f = self.g + self.h

    def __eq__(self, other):
        if self.node_a is None and other.node_a is None:
            return self.node_b == other.node_b
        elif self.node_a is None and other.node_a is not None:
            return False
        elif self.node_a is not None and other.node_a is None:
            return False

        return (self.node_a == other.node_a) and (self.node_b == other.node_b)

    def __hash__(self):
        return hash(self.node_a + self.node_b)

    def __repr__(self) -> str:
        return f" nodeA: {self.node_a}, nodeB: {self.node_b}, parent: {self.parent}, destination: {self.destination} "


# TEST CODE
if __name__ == "__main__":
    pass
