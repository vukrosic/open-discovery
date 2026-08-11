"""Candidate 005: preallocate adjacency slots before filling the graph."""


def connected_components(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """Return sorted connected components of an undirected graph."""
    degrees = [0] * n
    for left, right in edges:
        degrees[left] += 1
        degrees[right] += 1

    adjacency = [[0] * degree for degree in degrees]
    offsets = [0] * n
    for left, right in edges:
        adjacency[left][offsets[left]] = right
        offsets[left] += 1
        adjacency[right][offsets[right]] = left
        offsets[right] += 1

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
        components.append(sorted(component))

    return sorted(components, key=lambda component: component[0])
