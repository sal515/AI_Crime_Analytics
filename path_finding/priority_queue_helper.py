# # helper class for priority queues using heapq - https://docs.python.org/3/library/heapq.html
from path_finding.vertex import vertex as vtx
import itertools
import queue as q
from collections import defaultdict


class pq_helper:
    counter = itertools.count()

    # pq = q.PriorityQueue(-1) - infinite priority queue size

    @staticmethod
    def add_vertex(vertex: vtx, pq: q.PriorityQueue, vertex_finder_dict: defaultdict) -> None:
        vertex_key = str(hash(vertex))
        count = next(pq_helper.counter)
        vertex_entry = [vertex.f, count, vertex]
        # vertex_finder_dict[vertex_key] = vertex_entry
        vertex_finder_dict[vertex_key].append(vertex_entry)
        pq.put(vertex_entry)

    @staticmethod
    def remove_vertex(vertex_key: str, vertex_f, vertex_finder_dict: defaultdict) -> None:
        if vertex_key in vertex_finder_dict:
            if len(vertex_finder_dict[vertex_key]) < 2:
                vertex_finder_dict.pop(vertex_key)
                return

            index = itertools.count()
            for vertex_entry in vertex_finder_dict[vertex_key]:
                i = next(index)
                if vertex_entry[0] == vertex_f:
                    del vertex_finder_dict[vertex_key][i]

    @staticmethod
    def pop_vertex(pq: q.PriorityQueue, vertex_finder_dict: {}) -> vtx:
        if not pq.empty():
            out_vertex = pq.get()
            pq_helper.remove_vertex(str(hash(out_vertex[2])), out_vertex[0], vertex_finder_dict)
            return out_vertex[2]
