import itertools
import queue as q
import time

import numpy as np
from numpy import inf
from collections import defaultdict

from path_finding.node import node
from path_finding.vertex import vertex
from data_processing.data import data as dt
from path_finding.priority_queue_helper import pq_helper


class aStar:

    def __init__(self, start_xy: tuple, destination_xy: tuple, obstacles_array: [], data: dt) -> None:
        self.data = data
        self.obstacle_array = obstacles_array

        """ Path from vertices from start to destination """
        self.path = []
        self.total_cost_f = 0
        self.total_cost_g = 0
        self.total_cost_h = 0
        self.heuristic_estimates_each_vertex = []

        """ Get the lowest f value for next vertex using priority queue """
        self.open_priority_queue = q.PriorityQueue(-1)
        self.open_dict = defaultdict(list)

        """ List containing visited nodes to prevent cycling between visited nodes """
        self.closed_list = []
        self.closed_dict = {}

        """ Row and column values are generated from provided x and y coordinates """
        self.start_row, self.start_col = data.to_row_col_from_coord(start_xy[0], start_xy[1])
        self.destination_row, self.destination_col = data.to_row_col_from_coord(destination_xy[0], destination_xy[1])

        """ Created the start node and destination node to use in the vertices generation """
        self.start: node = node.create(self.start_row, self.start_col, data)
        self.destination: node = node.create(self.destination_row, self.destination_col, data)

        """ To get all possible adjacent nodes from a node - list of possible row and column translation """
        self.row_col_possibilities = [(1, -1), (1, 0), (1, 1), (0, -1), (0, 0), (0, 1), (-1, -1), (-1, 0), (-1, 1)]

    def run(self, data, timeout):
        timer_offset = time.perf_counter()

        """ Create start vertex no parent and add to closed closed list """
        if self.start is None or self.destination is None:
            raise Exception("Error: Start or Destination vertex was not created")

        """ Start vertex is inserted to the open priority queue - for nodes to be visited"""
        start_vertex = vertex(None, self.start, None, self.destination, None, None)
        pq_helper.add_vertex(start_vertex, self.open_priority_queue, self.open_dict)

        """ Creating destination vertex to check if it is blocked or not later on"""
        destination_vertex = vertex(None, self.destination, None, self.destination, None, None)

        while not self.open_priority_queue.empty():
            data.time_taken = time.perf_counter() - timer_offset
            if data.time_taken > timeout:
                break

            """ Get the vertex with the lowest f value from the open priority queue/ open list """
            current_vertex: vertex = pq_helper.pop_vertex(self.open_priority_queue, self.open_dict)

            """ add the current vertex removed from the open list to the closed list & dict """
            self.update_closed_list(current_vertex)

            """ Destination found if the vertex has the destination node, return path """
            if current_vertex.node_b == self.destination:
                self.data.path_found = True
                backtrace_vertex = current_vertex
                while not backtrace_vertex.node_b == self.start:
                    self.path.append(backtrace_vertex)
                    self.total_cost_f += backtrace_vertex.f
                    self.total_cost_g += backtrace_vertex.g
                    self.total_cost_h += backtrace_vertex.h
                    self.heuristic_estimates_each_vertex.append(backtrace_vertex.h)
                    backtrace_vertex = backtrace_vertex.parent

                """ Returning shortest path and cumulative costs f,g,h"""
                data.time_taken = time.perf_counter() - timer_offset
                return (round(self.total_cost_f, 3), round(self.total_cost_g, 3),
                        round(self.total_cost_h, 3)), self.path[::-1]

            """ Check if the start node is surrounded by blocked nodes, if so then exit"""
            if not self.is_path_possible(start_vertex):
                break

            """ Similar to the last check, do it for the destination node"""
            if not self.is_path_possible(destination_vertex):
                break

            """ Generate all the adjacent nodes from the current vertex's end node"""
            nodes = list(
                map(lambda x: node.create(current_vertex.node_b.row + x[0], current_vertex.node_b.col + x[1],
                                          self.data),
                    self.row_col_possibilities))

            """ Generate all the adjacent vertices from the current vertex using adjacent nodes"""
            index = itertools.count()
            vertices = list(
                map(lambda n, i: vertex(current_vertex.node_b, n, current_vertex, self.destination, i, nodes), nodes,
                    index))

            for v in vertices:
                """ The vertex is hashed and the hashed key is used to keep a open_dict of vertices"""
                """ The open_dict allows us to easily check if the vertex is already in the open list/priority queue"""

                v_key = str(hash(v))

                """ Checking if the one of the potential vertices are not eligible to be in the open list/priority_queue """
                if v.f == inf:
                    continue

                if v_key in self.closed_dict:
                    continue

                if v_key in self.open_dict:
                    for old_vertex in self.open_dict[v_key]:
                        if v.g > old_vertex[2].g:
                            continue

                """Add eligible vertices to the open list / priority queue"""
                pq_helper.add_vertex(v, self.open_priority_queue, self.open_dict)

        """ while loop ended and destination was not found """
        data.time_taken = time.perf_counter() - timer_offset
        if data.time_taken > timeout:
            print(f"* Timed-out: No Path Found from Start point to Destination point")
        else:
            print(f"* No Path Found from Start point to Destination point")
        return None, None

    def is_path_possible(self, vertex_to_check: vertex):
        """ Preliminary check for the starting and destination vertex"""
        """ Generate all the adjacent nodes for the start or destination point"""
        """ If all of the adjacent nodes are blocked, then there is no possible path """

        nodes = list(
            map(lambda x: node.create(vertex_to_check.node_b.row + x[0], vertex_to_check.node_b.col + x[1], self.data). \
                is_blocked if x is (node.create(vertex_to_check.node_b.row + x[0], vertex_to_check.node_b.col + x[1], \
                                                self.data)) is not None else 0, self.row_col_possibilities))

        if np.all(np.concatenate((np.array(nodes)[3:5], np.array(nodes)[6:8])) == 1):
            return False

        return True

    """" Helper functions """

    def update_closed_list(self, current_vertex):
        current_vertex_key = str(hash(current_vertex))
        if current_vertex_key in self.closed_dict:
            return
        self.closed_dict[current_vertex_key] = current_vertex
        self.closed_list.append(current_vertex)


# TEST CODE
if __name__ == "__main__":
    from data_processing.data import data as dt
