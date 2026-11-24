import heapq

def a_star_search(graph, heuristics, start, goal):
    counter = 0
    start_h = heuristics.get(start, 0)
    pq = [(start_h, counter, start, 0, [start])]
    best_g = {start: 0}
    visited = set()
    expanded_order = []
    nodes_generated = 1

    while pq:
        f_val, _, current, g_val, path = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)
        expanded_order.append(current)

        if current == goal:
            return {
                'path': path,
                'cost': g_val,
                'expanded_order': expanded_order,
                'nodes_expanded': len(expanded_order),
                'nodes_generated': nodes_generated
            }

        for neighbor, edge_cost in graph.get(current, []):
            tentative_g = g_val + edge_cost

            if neighbor not in best_g or tentative_g < best_g[neighbor]:
                best_g[neighbor] = tentative_g
                h_val = heuristics.get(neighbor, 0)
                f_score = tentative_g + h_val
                counter += 1
                nodes_generated += 1
                heapq.heappush(pq, (f_score, counter, neighbor, tentative_g, path + [neighbor]))

    return {
        'path': None,
        'cost': float('inf'),
        'expanded_order': expanded_order,
        'nodes_expanded': len(expanded_order),
        'nodes_generated': nodes_generated
    }

if __name__ == '__main__':
    graph = {
        'A': [('B', 2), ('C', 4)],
        'B': [('A', 2), ('D', 7), ('E', 3)],
        'C': [('A', 4), ('E', 1), ('F', 5)],
        'D': [('B', 7), ('S', 3)],
        'E': [('B', 3), ('C', 1), ('D', 2), ('S', 5)],
        'F': [('C', 5), ('S', 6)],
        'S': [('D', 3), ('E', 5), ('F', 6)]
    }

    heuristics = {
        'A': 6,
        'B': 4,
        'C': 4,
        'D': 2,
        'E': 3,
        'F': 4,
        'S': 0
    }

    start = 'B'
    goal = 'S'

    result = a_star_search(graph, heuristics, start, goal)
    print("Optimal Path    :", ' -> '.join(result['path']) if result['path'] else 'No path')
    print("Total Cost      :", result['cost'])
    print("Expansion Order :", result['expanded_order'])
    print("Nodes Expanded  :", result['nodes_expanded'])
    print("Nodes Generated :", result['nodes_generated'])
