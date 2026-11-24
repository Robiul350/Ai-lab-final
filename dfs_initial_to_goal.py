def dfs(graph, start, goal):
    stack = [[start]]
    visited = set()
    visited_order = []

    while stack:
        path = stack.pop()
        current_node = path[-1]

        if current_node not in visited:
            visited.add(current_node)
            visited_order.append(current_node)

            if current_node == goal:
                return path, visited_order

            for neighbor in reversed(graph.get(current_node, [])):
                if neighbor not in visited:
                    stack.append(path + [neighbor])

    return None, visited_order

if __name__ == '__main__':
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F', 'G'],
        'D': ['H', 'I'],
        'E': ['J', 'K'],
        'F': ['L', 'M'],
        'G': ['N', 'O'],
        'H': ['P', 'Q'],
        'I': ['R', 'S'],
        'J': ['T', 'U'],
        'K': ['V', 'W'],
        'L': ['X', 'Y'],
        'M': ['Z'],
        'N': [],
        'O': [],
        'P': [],
        'Q': [],
        'R': [],
        'S': [],
        'T': [],
        'U': [],
        'V': [],
        'W': [],
        'X': [],
        'Y': [],
        'Z': []
    }

    start = 'A'
    goal = 'S'

    path, order = dfs(graph, start, goal)
    print("Path Found    :", ' -> '.join(path) if path else 'No path')
    print("Visited Order :", order)
