"""Pinned bounded-cycle search baseline adapted from NetworkX.

Source: NetworkX ``networkx/algorithms/cycles.py`` at commit
13fa8e5dde7e25af268568b4e13cb61f352baa2e (2026-08-10).

Copyright (c) 2004-2026, NetworkX Developers.
Licensed under the BSD 3-Clause License; see LICENSE.networkx.txt.
"""

from collections import defaultdict


class _NeighborhoodCache(dict):
    """Cache adjacency iterables as lists, matching the upstream helper."""

    def __init__(self, graph):
        self.graph = graph

    def __missing__(self, node):
        neighbors = self[node] = list(self.graph[node])
        return neighbors


def bounded_cycle_search(graph, path, length_bound):
    """Yield simple directed cycles beginning with ``path`` within the bound."""

    graph = _NeighborhoodCache(graph)
    lock = {node: 0 for node in path}
    blocked = defaultdict(set)
    start = path[0]
    stack = [iter(graph[path[-1]])]
    bound_stack = [length_bound]
    while stack:
        neighbors = stack[-1]
        for neighbor in neighbors:
            if neighbor == start:
                yield path[:]
                bound_stack[-1] = 1
            elif len(path) < lock.get(neighbor, length_bound):
                path.append(neighbor)
                bound_stack.append(length_bound)
                lock[neighbor] = len(path)
                stack.append(iter(graph[neighbor]))
                break
        else:
            stack.pop()
            node = path.pop()
            bound = bound_stack.pop()
            if bound_stack:
                bound_stack[-1] = min(bound_stack[-1], bound)
            if bound < length_bound:
                relax_stack = [(bound, node)]
                while relax_stack:
                    bound, current = relax_stack.pop()
                    if lock.get(current, length_bound) < length_bound - bound + 1:
                        lock[current] = length_bound - bound + 1
                        relax_stack.extend(
                            (bound + 1, neighbor)
                            for neighbor in blocked[current].difference(path)
                        )
            else:
                for neighbor in graph[node]:
                    blocked[neighbor].add(node)
