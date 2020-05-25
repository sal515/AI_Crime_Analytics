from path_finding.node import node
from path_finding.priority_queue_helper import pq_helper
import queue as q


class aStar:

    def __init__(self, start, destination, obstacles_array) -> None:
        # eg.
        # start -> node(None,None,  (0,0))
        # destination -> node(None, None, (9,3))

        self.open_priority_queue = q.PriorityQueue(-1)
        self.open_map = {}
        # self.open_priority_queue = []
        self.closed_list = []
        self.closed_map = {}

        self.obst_arr = obstacles_array
        self.start: node = node(parent=None, destination=destination, position=start)
        self.destination: node = node(parent=None, destination=destination, position=destination)

        self.node_possibilities = [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (1, 1), (-1, -1), (1, -1)]

    def run(self):
        pq_helper.add_node(self.start, self.open_priority_queue, self.open_map)

        while not self.open_priority_queue.empty():
            # get current node from openList with lowest f
            # remove the current node from the open list & map
            current_node: node = pq_helper.pop_node(self.open_priority_queue, self.open_map)
            # add the current node to the closed list & map
            self.closed_map[str(hash(current_node))] = current_node
            self.closed_list.append(current_node)

            if current_node == self.destination:
                # FIXME: goal state found - use closed list to find shortest path to goal
                break

            for possible_node in self.node_possibilities:
                adjacent_node = self.get_adjacent_node(current_node, possible_node)

                if str(hash(adjacent_node)) in self.closed_map:
                    continue

                if (str(hash(adjacent_node)) in self.open_map) and (
                        adjacent_node.g > self.open_map[str(hash(adjacent_node))].g):
                    continue

                # FIXME duplicate - How?
                # self.open_map[str(hash(adjacent_node))] = adjacent_node
                pq_helper.add_node(adjacent_node, self.open_priority_queue, self.open_map)

    def get_adjacent_node(self, current_node: node, possible_node):
        return node(current_node, self.destination,
                    (current_node.position[0] + possible_node[0], current_node.position[1] + possible_node[1]))
