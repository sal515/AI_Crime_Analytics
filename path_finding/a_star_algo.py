import itertools

from path_finding.node import node
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

    def get_adjacent_node(self, current_node: node, possible_node):
        return node(current_node, self.destination,
                    (current_node.position[0] + possible_node[0], current_node.position[1] + possible_node[1]))

# TEST CODE
if __name__ == "__main__":
    pass