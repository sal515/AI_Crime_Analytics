import itertools
import queue as q

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

        # FIXME: Check anything related to the open dict and duplicate keys
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

    def run(self):
        # FIXME
        """ insert forbidden vertices to the closed list """
        self.update_forbidden_vertices(self.data)

        """ Create start vertex no parent and add to closed closed list """
        if self.start is None:
            raise Exception("Error: Start vertex was not created")

        """ Start vertex is inserted to the open priority queue - for nodes to be visited"""
        start_vertex = vertex(None, self.start, None, self.destination, None, None)
        pq_helper.add_vertex(start_vertex, self.open_priority_queue, self.open_dict)

        while not self.open_priority_queue.empty():
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
                return (round(self.total_cost_f, 3), round(self.total_cost_g, 3),
                        round(self.total_cost_h, 3)), self.path[::-1]

            """ Generate all the adjacent nodes from the current vertex's end node"""
            nodes = list(
                map(lambda x: node.create(current_vertex.node_b.row + x[0], current_vertex.node_b.col + x[1],
                                          self.data),
                    self.row_col_possibilities))

            # Test print all nodes
            # [print(i) for i in zip(enumerate(nodes)) if i is not None]

            """ Generate all the adjacent vertices from the current vertex using adjacent nodes"""
            index = itertools.count()
            vertices = list(
                map(lambda n, i: vertex(current_vertex.node_b, n, current_vertex, self.destination, i, nodes), nodes,
                    index))

            # fixme: Check blocked vertices for start

            # fixme: Check blocked vertices for destination

            for v in vertices:
                """ The vertex is hashed and the hashed key is used to keep a open_dict of vertices"""
                """ The open_dict allows us to easily check if the vertex is already in the open list/priority queue"""

                v_key = str(hash(v))

                # FIXME: Check if the node is within range
                # FIXME: Check if the node is blocked or not
                # if str(hash(v)) in self.forbidden_vertices:
                #     continue

                """ Checking if the one of the potential vertices are not eligible to be in the open list/priority_queue """
                if v.f == inf:
                    continue

                if v_key in self.closed_dict:
                    continue

                if v_key in self.open_dict:
                    for node_entry in self.open_dict[v_key]:
                        if v.g > node_entry[2].g:
                            continue

                """Add eligible vertices to the open list / priority queue"""
                pq_helper.add_vertex(v, self.open_priority_queue, self.open_dict)

        """ while loop ended and destination was not found """
        print("No Path Found from Start point to Destination point")
        return None, None

    """" Helper functions """

    def update_forbidden_vertices(self, data: dt):
        r = 0
        for c in range(0, self.data.cols - 1):
            node_a: node = node.create(r, c, data)
            node_b: node = node.create(r, c + 1, data)
            forbidden_vertex = vertex(node_a, node_b, None, None, None, None)
            self.update_closed_list(forbidden_vertex)
            # self.forbidden_vertices[str(hash(forbidden_vertex))] = ((r, c), (r, c + 1))
            # self.forbidden_vertices[str(hash(forbidden_vertex))] = forbidden_vertex
        c = 0
        for r in range(0, self.data.rows - 1):
            node_a: node = node.create(r, c, data)
            node_b: node = node.create(r + 1, c, data)
            forbidden_vertex = vertex(node_a, node_b, None, None, None, None)
            self.update_closed_list(forbidden_vertex)
            # self.forbidden_vertices[str(hash(forbidden_vertex))] = ((r, c), (r + 1, c))
            # self.forbidden_vertices[str(hash(forbidden_vertex))] = forbidden_vertex

    def update_closed_list(self, current_vertex):
        current_vertex_key = str(hash(current_vertex))
        if current_vertex_key in self.closed_dict:
            return
        self.closed_dict[current_vertex_key] = current_vertex
        self.closed_list.append(current_vertex)


# TEST CODE
if __name__ == "__main__":
    from data_processing.data import data as dt

    obstacles_array_50_percent = [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1,
                                  0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
                                  1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1,
                                  1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                                  1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0,
                                  0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
                                  0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0,
                                  0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0,
                                  1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1,
                                  0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1,
                                  0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0,
                                  0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1]

    dt = dt(0.002, 0.0001, 50, "..\\data\\Shape\\crime_dt.shp")

    dt.obstacles_arr = obstacles_array_50_percent

    # Test node
    # origin_node = node(dt.lower_x_bound + 1 * 0.002, dt.lower_y_bound + 1 * 0.002, dt)
    # destination_node = node(dt.lower_x_bound + 2 * 0.002, dt.lower_y_bound + 6 * 0.002, dt)
    #
    # node1 = node(dt.lower_x_bound + -1 * 0.002, dt.lower_y_bound + 6 * 0.002, dt)
    # node2 = node(dt.lower_x_bound + 2 * 0.002, dt.lower_y_bound + 6 * 0.002, dt)
    # node3 = node(dt.lower_x_bound + 2 * 0.002, dt.lower_y_bound + 6 * 0.002, dt)

    origin_node = node.create(0, 0, dt)
    destination_node = node.create(4, 2, dt)

    node1 = node.create(1, 1, dt)
    node2 = node.create(2, 1, dt)
    node3 = node.create(2, 2, dt)

    print("start node: ", origin_node)
    print("destination node: ", destination_node)
    print(origin_node == destination_node)
    print(origin_node == origin_node)

    # Test vertex
    v1 = vertex(None, origin_node, None, destination_node, None, None)
    v2 = vertex(origin_node, node1, v1, destination_node, None, None)
    v3 = vertex(node1, node2, v2, destination_node, None, None)
    v4 = vertex(node2, node3, v3, destination_node, None, None)

    print("(v1 == v1)", (v1 == v1))
    print("(v1 == v2)", (v1 == v2))
    print("(v2 == v3)", (v2 == v3))
    print("(v3 == v4)", (v3 == v4))

    # Generate possibles nodes
    # node_possibilities = [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (1, 1), (-1, -1), (1, -1)]
    # node_possibilities = [(1, -1), (1, 0), (1, 1), (0, -1), (0, 0), (0, 1), (-1, -1), (-1, 0), (-1, 1)]

    row_col_possibilities = [(1, -1), (1, 0), (1, 1), (0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1)]

    current_node = v1.node_b
    node_possibilities = list(
        map(lambda x: node.create(current_node.row + x[0], current_node.col + x[1], dt), row_col_possibilities))

    [print(i) for i in zip(enumerate(node_possibilities)) if i is not None]

    index = itertools.count()
    vertices_possible = list(
        map(lambda x, i: vertex(current_node, x, v1, destination_node, i, node_possibilities), node_possibilities,
            index))

    [print(i) for i in zip(enumerate(vertices_possible))]

    [print(hash(i)) for i in zip(enumerate(vertices_possible)) if i is not None]

    pass
