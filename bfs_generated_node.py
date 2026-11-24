from collections import deque

def count_generated_nodes_bfs(graph, start, goal):
    if start == goal:
        return 1, [start]

    queue = deque([start])
    visited = set([start])
    nodes_generated = 1

    while queue:
        current = queue.popleft()

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                nodes_generated += 1
                queue.append(neighbor)

                if neighbor == goal:
                    return nodes_generated, visited

    return nodes_generated, visited

def theoretical_bfs_nodes(b, d):
    if b == 1:
        return d + 1
    return (b**(d + 1) - 1) // (b - 1)

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
    b = 2
    d = 4

    total_generated, visited_nodes = count_generated_nodes_bfs(graph, start, goal)
    print("Actual Generated Nodes      :", total_generated)
    print("Theoretical Generated (b=2, d=4):", theoretical_bfs_nodes(b, d))
