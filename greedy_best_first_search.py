import heapq

def greedy_best_first_search(graph, heuristics, start, goal):
    counter = 0
    pq = [(heuristics[start], counter, start, [start])]
    visited = set()
    expanded_order = []
    nodes_generated = 1

    while pq:
        h_val, _, current, path = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)
        expanded_order.append(current)

        if current == goal:
            return {
                'path': path,
                'expanded_order': expanded_order,
                'nodes_expanded': len(expanded_order),
                'nodes_generated': nodes_generated
            }

        for neighbor, _ in graph.get(current, []):
            if neighbor not in visited:
                counter += 1
                nodes_generated += 1
                heapq.heappush(pq, (heuristics.get(neighbor, float('inf')), counter, neighbor, path + [neighbor]))

    return {
        'path': None,
        'expanded_order': expanded_order,
        'nodes_expanded': len(expanded_order),
        'nodes_generated': nodes_generated
    }

if __name__ == '__main__':
    graph = {
        'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
        'Zerind': [('Arad', 75), ('Oradea', 71)],
        'Oradea': [('Zerind', 71), ('Sibiu', 151)],
        'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
        'Timisoara': [('Arad', 118), ('Lugoj', 111)],
        'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
        'Mehadia': [('Lugoj', 70), ('Drobeta', 75)],
        'Drobeta': [('Mehadia', 75), ('Craiova', 120)],
        'Craiova': [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
        'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
        'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
        'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
        'Bucharest': [('Fagaras', 211), ('Pitesti', 101)]
    }

    heuristics = {
        'Arad': 366,
        'Zerind': 374,
        'Oradea': 380,
        'Sibiu': 253,
        'Timisoara': 329,
        'Lugoj': 244,
        'Mehadia': 241,
        'Drobeta': 242,
        'Craiova': 160,
        'Rimnicu Vilcea': 193,
        'Fagaras': 176,
        'Pitesti': 100,
        'Bucharest': 0
    }

    start = 'Arad'
    goal = 'Bucharest'

    result = greedy_best_first_search(graph, heuristics, start, goal)
    print("Path Found      :", ' -> '.join(result['path']) if result['path'] else 'No path')
    print("Expansion Order :", result['expanded_order'])
    print("Nodes Expanded  :", result['nodes_expanded'])
    print("Nodes Generated :", result['nodes_generated'])
