import itertools

from path_finding.node import node
from path_finding.vertex import vertex
from path_finding.priority_queue_helper import pq_helper
import queue as q
from collections import defaultdict


class aStar:

    def __init__(self, start, destination, obstacles_array, data) -> None:
        # eg.
        # start -> node(None,None,  (0,0))
        # destination -> node(None, None, (9,3))

        self.path = []

        self.open_priority_queue = q.PriorityQueue(-1)
        # self.open_dict = {}
        # FIXME: Check anything related to the open dict and duplicate keys
        self.open_dict = defaultdict(list)
        self.closed_list = []
        self.closed_dict = {}

        # assuming the boundary is of a square or rectangle
        self.data = data
        # self.rows = data.rows
        # self.cols = data.cols
        # self.forbidden_nodes = (self.rows * 2 + self.cols * 2) - 4
        self.forbidden_nodes_dict = {}

        self.obstacle_array = obstacles_array
        self.start: node = node(parent=None, destination=destination, position=start)
        self.destination: node = node(parent=None, destination=destination, position=destination)

        self.node_possibilities = [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (1, 1), (-1, -1), (1, -1)]

    def run(self):
        # insert blocked/corner nodes to the closed list
        self.update_forbidden_nodes()

        pq_helper.add_node(self.start, self.open_priority_queue, self.open_dict)

        while not self.open_priority_queue.empty():
            # get current node from openList with lowest f
            # remove the current node from the open list & dict
            current_node: node = pq_helper.pop_node(self.open_priority_queue, self.open_dict)

            # FIXME
            # add the current node to the closed list & dict
            self.update_closed_list(current_node)

            if current_node == self.destination:
                backtrace_node = current_node
                while not backtrace_node == self.start:
                    self.path.append(backtrace_node)
                    backtrace_node = backtrace_node.parent
                # return shortest path
                return self.path[::-1]

            for possible_node in self.node_possibilities:
                adjacent_node = self.get_adjacent_node(current_node, possible_node)
                adjacent_node_key = str(hash(adjacent_node))

                # FIXME: Check if the node is within range
                # FIXME: Check if the node is blocked or not
                if str(hash(adjacent_node)) in self.forbidden_nodes_dict:
                    continue

                if adjacent_node_key in self.closed_dict:
                    continue

                # Fixme : duplicate keys for the map
                if adjacent_node_key in self.open_dict:
                    for node_entry in self.open_dict[adjacent_node_key]:
                        if adjacent_node.g > node_entry[2].g:
                            continue

                pq_helper.add_node(adjacent_node, self.open_priority_queue, self.open_dict)

    # === Helper functions ===

    def update_forbidden_nodes(self):
        for r in (0, self.data.rows - 1):
            for c in range(0, self.data.cols):
                # self.obstacle_array[self.data.to_index(r,c,self.cols)]
                # self.update_closed_list(node(None, None, (r, c)))
                self.forbidden_nodes_dict[str(hash(node(None, None, (r, c))))] = (r, c)

        for c in (0, self.data.cols - 1):
            for r in range(0, self.data.rows):
                # self.obstacle_array[self.data.to_index(r,c,self.cols)]
                # self.update_closed_list(node(None, None, (r, c)))
                self.forbidden_nodes_dict[str(hash(node(None, None, (r, c))))] = (r, c)

        blocked_grids_r_c = [self.data.to_row_col_from_index(i, self.data.cols) for i in range(len(self.obstacle_array))
                             if
                             self.obstacle_array[i] == 0]
        for r_c in blocked_grids_r_c:
            # self.update_closed_list(node(None, None, r_c))
            self.forbidden_nodes_dict[str(hash(node(None, None, r_c)))] = r_c

    def update_closed_list(self, current_node):
        current_node_key = str(hash(current_node))
        if current_node_key in self.closed_dict:
            return
        self.closed_dict[current_node_key] = current_node
        self.closed_list.append(current_node)

    # def get_adjacent_node(self, current_node: node, possible_node):
    #     return node(current_node, self.destination,
    #                 (current_node.position[0] + possible_node[0], current_node.position[1] + possible_node[1]))


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

    dt = dt(0.002, 0.0001, 50, None, None, "..\\data\\Shape\\crime_dt.shp")

    dt.obstacles_arr = obstacles_array_50_percent

    # Test node
    origin_node = node(dt.lower_x_bound + 1 * 0.002, dt.lower_y_bound + 1 * 0.002, dt)
    destination_node = node(dt.lower_x_bound + 2 * 0.002, dt.lower_y_bound + 6 * 0.002, dt)

    node1 = node(dt.lower_x_bound + -1 * 0.002, dt.lower_y_bound + 6 * 0.002, dt)
    node2 = node(dt.lower_x_bound + 2 * 0.002, dt.lower_y_bound + 6 * 0.002, dt)
    node3 = node(dt.lower_x_bound + 2 * 0.002, dt.lower_y_bound + 6 * 0.002, dt)

    print("start node: ", origin_node)
    print("destination node: ", destination_node)
    print(origin_node == destination_node)
    print(origin_node == origin_node)

    # Test vertex
    v1 = vertex(None, origin_node, None, destination_node)
    v2 = vertex(origin_node, node1, v1, destination_node)
    v3 = vertex(node1, node2, v2, destination_node)
    v4 = vertex(node2, node3, v3, destination_node)

    print("(v1 == v1)", (v1 == v1))
    print("(v1 == v2)", (v1 == v2))
    print("(v2 == v3)", (v2 == v3))
    print("(v3 == v4)", (v3 == v4))

    # Generate possibles nodes
    # node_possibilities = [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (1, 1), (-1, -1), (1, -1)]
    node_possibilities = [(1, -1), (1, 0), (1, 1), (0, -1), (0, 0), (0, 1), (-1, -1), (-1, 0), (-1, 1)]

    current_node = v1.node_b
    all_possible_nodes = []

    for i in node_possibilities:
        new_x_y = dt.to_coordinate_from_row_col((current_node.row + i[0], current_node.col + i[1]))
        all_possible_nodes.append(node(new_x_y[0], new_x_y[1], dt))

    # all_possible_nodes = list(
    #     map(lambda x:, node_possibilities))

    [print(i) for i in zip(enumerate(all_possible_nodes))]

    # p_origin = point(dt.start, dt)
    # p_destination = point(dt.destination, dt)
    #
    # p1 = point((dt.lower_x_bound + 1 * 0.00200001, dt.lower_y_bound + 1 * 0.00200001), dt)
    # p2 = point((dt.lower_x_bound + 2 * 0.00200001, dt.lower_y_bound + 2 * 0.00200001), dt)
    # p3 = point((dt.lower_x_bound + 5 * 0.00200001, dt.lower_y_bound + 9 * 0.00200001), dt)
    #
    # print(p_origin)
    # print(p_destination)
    #
    # print((p_origin + p_destination))
    # print(hash(p_origin + p_destination))
    # print((p_destination + p_origin))
    # print(hash(p_destination + p_origin))
    #
    # print((p_origin == p_destination))
    # print((p_origin == p_origin))
    #
    # # Vertex Test
    # v1 = vertex(None, p_destination, p_origin, p1)
    # v2 = vertex(v1, p_destination, p1, p2)
    # v3 = vertex(v2, p_destination, p2, p3)
    #
    # print("v1: ", v1)
    # print("v2: ", v2)
    # print("v3: ", v3)
    #
    # print("v1: ", hash(v1))
    # print("v1: ", hash(v1))
    # print("v2: ", hash(v2))
    # print("v3: ", hash(v3))
    #
    # # vertex generation from a point
    # print("p origin: ", p_origin)
    #
    # # sgl = dt.square_grid_length+dt.square_grid_length_padding
    # sgl = dt.square_grid_length
    #
    # print("origin:", (dt.start[0], dt.start[1]))
    # print("origin:", (dt.min_x, dt.min_y))
    #
    # possibilities = [(-sgl, 0), (sgl, 0), (0, sgl), (0, -sgl), (-sgl, sgl), (sgl, sgl), (-sgl, -sgl), (sgl, -sgl)]
    #
    # possibilities_calc = list(map(lambda i: (dt.start[0] + i[0], dt.start[1] + i[1]), possibilities))
    #
    # point_possibilities = list(map(lambda i: point((dt.start[0] + i[0], dt.start[1] + i[1]), dt), possibilities))
    #
    # # [print(i, (dt.start)) for i in zip(enumerate(point_possibilities),(possibilities))]
    #
    # [print(i, (dt.start)) for i in zip(enumerate(point_possibilities), possibilities, possibilities_calc)]

    pass

    pass
