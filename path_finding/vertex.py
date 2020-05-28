from numpy import inf
from path_finding.node import node
import math


class vertex:

    def __init__(self, node_a: node, node_b: node, parent, destination: node, vertex_pos: int,
                 possible_nodes: [node]) -> None:
        """ vertex cls holds the start node and and end node of a vertex on the grid """

        self.parent = parent
        self.destination: node = destination

        """ list of possible nodes around the end of a vertex is used to calculate cost g """
        self.possible_nodes: [node] = possible_nodes
        self.vertex_pos = vertex_pos

        """ node a is the start node of a vertex and node b is the end node of the vertex"""
        self.node_a: node = node_a
        self.node_b: node = node_b

        """ used to create the initial vertex, since the vertex does not have a parent vertex  """
        self.g = 0
        self.h = 0
        self.f = 0

        """ logic to calculate the cost g, to create a new vertex composed of node_a to node_b"""
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
                # itself
                self.g = 0

            elif self.vertex_pos == 5:
                # right
                self.calculate_g_straight(4, 7)

            elif self.vertex_pos == 6:
                # diagonal bottom left
                self.calculate_g_diagonal(6)

            elif self.vertex_pos == 7:
                # down
                self.calculate_g_straight(6, 7)

            elif self.vertex_pos == 8:
                # diagonal bottom right
                self.calculate_g_diagonal(7)

            """ the Heuristic function (h) is calculated as the distance between two points on the grid"""
            """ this heuristic function is admissible because it never overestimates"""
            """ it calculates straight line distance between two points 
            which is the shortest distance between the points"""
            """ thus the heuristic function satisfies h(n) <= c(n) for all nodes n"""
            """ which implies the heuristic function cost is always lower than the actual cost"""

            self.h = inf
            if node_b is not None:
                row_length = abs(abs(self.node_b.row) - abs(self.destination.row))
                col_length = abs(abs(self.node_b.col) - abs(self.destination.col))
                self.h = math.sqrt(pow(row_length, 2) + pow(col_length, 2))

            """ total cost of the new vertex to be created is the sum of g and h """
            self.f = self.g + self.h

            self.f = round(self.f, 4)
            self.g = round(self.g, 4)
            self.h = round(self.h, 4)

    def calculate_g_straight(self, node_number1: int, node_number2: int):
        self.g = self.parent.g + 1

        # checks blocked nodes
        if not self.is_none(node_number1) and not self.is_none(node_number2):

            if self.is_blocked(node_number1) and self.is_blocked(node_number2):
                self.g = inf

            elif self.is_blocked(node_number1) and not self.is_blocked(node_number2):
                self.g = self.parent.g + 1.3

            elif not self.is_blocked(node_number1) and self.is_blocked(node_number2):
                self.g = self.parent.g + 1.3

        # checks none nodes
        elif self.is_none(node_number1) and self.is_none(node_number2):
            self.g = inf

        elif self.is_none(node_number1) and not self.is_none(node_number2):
            # left boundary edge
            self.g = inf

        elif not self.is_none(node_number1) and self.is_none(node_number2):
            # right boundary edge
            self.g = inf


    def is_blocked(self, node_number):
        return self.possible_nodes[node_number].is_blocked

    def is_none(self, node_number):
        return self.possible_nodes[node_number] is None or self.possible_nodes[node_number].isNone

    def calculate_g_diagonal(self, node_number: int):
        self.g = self.parent.g + 1.5
        if not self.is_none(node_number):
            if self.possible_nodes[node_number].is_blocked:
                self.g = inf

        elif self.is_none(node_number):
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
        return f" node_a: {self.node_a}, node_b: {self.node_b}, f_g_h: {(self.f, self.g, self.h)}, parent: {self.parent}\n"


# TEST CODE
if __name__ == "__main__":
    pass
