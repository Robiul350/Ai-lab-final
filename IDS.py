def dls(graph, node, goal, depth):
    if node == goal:
        return True

    if depth == 0:
        return False

    for child in graph.get(node, []):
        if dls(graph, child, goal, depth - 1):
            return True

    return False


def ids(graph, start, goal, max_depth):
    for depth in range(max_depth + 1):
        print("Searching at depth:", depth)

        if dls(graph, start, goal, depth):
            print("Goal found at depth:", depth)
            return True

    print("Goal not found")
    return False


graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': [],
    'E': [],
    'F': [],
    'G': []
}


ids(graph, 'A', 'G', 3)