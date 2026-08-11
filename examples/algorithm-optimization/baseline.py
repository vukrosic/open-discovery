"""Reference implementation for AL-01."""


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
        components.append(sorted(component))

    return sorted(components, key=lambda component: component[0])
