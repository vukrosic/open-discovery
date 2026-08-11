"""Candidate 004: build components with union-find instead of an adjacency DFS."""


def connected_components(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """Return sorted connected components of an undirected graph."""
    parent = list(range(n))
    size = [1] * n

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in edges:
        left_root = find(left)
        right_root = find(right)
        if left_root == right_root:
            continue
        if size[left_root] < size[right_root]:
            left_root, right_root = right_root, left_root
        parent[right_root] = left_root
        size[left_root] += size[right_root]

    grouped: dict[int, list[int]] = {}
    # Iterating vertices in order makes every grouped component sorted without
    # a second per-component sort.
    for vertex in range(n):
        root = find(vertex)
        grouped.setdefault(root, []).append(vertex)

    return sorted(grouped.values(), key=lambda component: component[0])
