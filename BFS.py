from collections import deque

def bfs(graph, start, goal):
    queue = deque([[start]])
    visited = set([start])
    visited_order = []

    while queue:
        path = queue.popleft()
        current_node = path[-1]
        visited_order.append(current_node)

        if current_node == goal:
            return path, visited_order

        for neighbor in graph.get(current_node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

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
    goal = 'X'

    path, order = bfs(graph, start, goal)
    print("Path Found    :", ' -> '.join(path) if path else 'No path')
    print("Visited Order :", order)
