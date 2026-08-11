"""Candidate 002: skip an unnecessary component sort when traversal is ordered."""


def _normalize_component(component: list[int]) -> list[int]:
    """Sort only when the traversal did not already produce ascending values."""
    for previous, current in zip(component, component[1:]):
        if previous > current:
            component.sort()
            break
    return component


def connected_components(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """Return sorted connected components of an undirected graph."""
    adjacency = [[] for _ in range(n)]
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)

    seen = [False] * n
    components: list[list[int]] = []
    for start in range(n):
        if seen[start]:
            continue
        stack = [start]
        seen[start] = True
        component: list[int] = []
        while stack:
            vertex = stack.pop()
            component.append(vertex)
            for neighbour in adjacency[vertex]:
                if not seen[neighbour]:
                    seen[neighbour] = True
                    stack.append(neighbour)
        components.append(_normalize_component(component))

    return sorted(components, key=lambda component: component[0])
