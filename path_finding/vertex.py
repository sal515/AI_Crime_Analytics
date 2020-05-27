from numpy import inf
from path_finding.node import node
import math


class vertex:

    def __init__(self, node_a: node, node_b: node, parent, destination: node, vertex_pos: int, possible_nodes: [node]) -> None:
        self.parent = parent
        self.destination: node = destination

        self.vertex_pos = vertex_pos
        self.possible_nodes: [node] = possible_nodes

        self.node_a: node = node_a
        self.node_b: node = node_b

        self.g = 0
        self.h = 0
        self.f = 0

        if self.parent is not None and self.vertex_pos is not None:
            if self.vertex_pos == 0:
                # diagonal top left
                self.calculate_g_diagonal(3)

            elif self.vertex_pos == 1:
                # up
                self.calculate_g_straight(3, 4)

            elif self.vertex_pos == 2:
                # diagonal top right
                self.calculate_g_diagonal(4)

            elif self.vertex_pos == 3:
                # left
                self.calculate_g_straight(3, 6)

            elif self.vertex_pos == 4:
                # right
                self.calculate_g_straight(4, 7)

            elif self.vertex_pos == 5:
                # diagonal bottom left
                self.calculate_g_diagonal(6)

            elif self.vertex_pos == 6:
                # down
                self.calculate_g_straight(6, 7)

            elif self.vertex_pos == 7:
                # diagonal bottom right
                self.calculate_g_diagonal(7)

            self.h = inf
            if node_b is not None:
                row_length = abs(abs(self.node_b.row) - abs(self.destination.row))
                col_length = abs(abs(self.node_b.col) - abs(self.destination.col))
                self.h = math.sqrt(pow(row_length, 2) + pow(col_length, 2))

            self.f = self.g + self.h

            self.f = round(self.f, 3)
            self.g = round(self.g, 3)
            self.h = round(self.h, 3)

    def calculate_g_straight(self, node_number1: int, node_number2: int):
        self.g = self.parent.g + 1
        if (self.possible_nodes[node_number1] is None or self.possible_nodes[node_number1].is_blocked) and \
                (self.possible_nodes[node_number2] is None or self.possible_nodes[node_number2].is_blocked):
            self.g = inf

        elif (self.possible_nodes[node_number1] is None or self.possible_nodes[node_number1].is_blocked) and \
                (self.possible_nodes[node_number2] is not None or not self.possible_nodes[node_number2].is_blocked):
            self.g = self.parent.g + 1.3

        elif (self.possible_nodes[node_number1] is not None or not self.possible_nodes[node_number1].is_blocked) and \
                (self.possible_nodes[node_number2] is None or self.possible_nodes[node_number2].is_blocked):
            self.g = self.parent.g + 1.3

    def calculate_g_diagonal(self, node_number: int):
        self.g = self.parent.g + 1.5
        if self.possible_nodes[node_number] is None or self.possible_nodes[node_number].is_blocked:
            self.g = inf

    def __eq__(self, other):
        if self.node_a is None and other.node_a is None:
            return self.node_b == other.node_b
        elif self.node_a is None and other.node_a is not None:
            return False
        elif self.node_a is not None and other.node_a is None:
            return False

        return (self.node_a == other.node_a) and (self.node_b == other.node_b)

    def __hash__(self):
        if self.node_a is None:
            return hash(self.node_b + self.node_a)

        return hash(self.node_a + self.node_b)

    def __repr__(self) -> str:
        return f" node_a: {self.node_a}, node_b: {self.node_b}, f_g_h: {(self.f, self.g, self.h)}, parent: {(self.parent)}\n"

    # def __repr__(self) -> str:
    #     return f" node_a: {self.node_a}, node_b: {self.node_b}, f_g_h: {(self.f, self.g, self.h)}, parent: {self.parent}, destination: {self.destination}, vertex_pos: {self.vertex_pos} "


# TEST CODE
if __name__ == "__main__":
    pass
