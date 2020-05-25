# # helper class for priority queues using heapq - https://docs.python.org/3/library/heapq.html
import itertools
from path_finding.node import node
import queue as q


class pq_helper:
    counter = itertools.count()

    # pq = q.PriorityQueue(-1) - infinite priority queue size

    @staticmethod
    def add_node(node: node, pq: q.PriorityQueue, node_finder_dict: {}) -> None:
        node_key = str(hash(node))
        count = next(pq_helper.counter)
        node_entry = [node.f, count, node]
        node_finder_dict[node_key] = node_entry
        pq.put(node_entry)

    @staticmethod
    def remove_node(node_key: str, node_finder_dict: {}) -> None:
        if node_key in node_finder_dict:
            node_finder_dict.pop(node_key)

    @staticmethod
    def pop_node(pq: q.PriorityQueue, node_finder_dict: {}) -> node:
        if not pq.empty():
            out_node = pq.get()
            pq_helper.remove_node(str(hash(out_node[2])), node_finder_dict)
            return out_node[2]
