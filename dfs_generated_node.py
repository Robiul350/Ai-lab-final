def count_generated_nodes_dfs(graph, start, goal):
    if start == goal:
        return 1, 1, [start]

    stack = [start]
    visited = set()
    expanded_order = []
    nodes_generated = 1

    while stack:
        current = stack.pop()

        if current not in visited:
            visited.add(current)
            expanded_order.append(current)

            if current == goal:
                return nodes_generated, len(expanded_order), expanded_order

            for neighbor in reversed(graph.get(current, [])):
                if neighbor not in visited:
                    nodes_generated += 1
                    stack.append(neighbor)

    return nodes_generated, len(expanded_order), expanded_order

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

    generated_count, expanded_count, order = count_generated_nodes_dfs(graph, start, goal)
    print("Expansion Order         :", order)
    print("Number of Expanded Nodes:", expanded_count)
    print("Number of Generated Nodes:", generated_count)
