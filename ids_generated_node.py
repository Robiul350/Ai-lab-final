def dls_count_generated(graph, node, goal, depth_limit, path, stats):
    stats['expanded'] += 1
    current_path = path + [node]

    if node == goal:
        return current_path

    if depth_limit <= 0:
        return None

    for neighbor in graph.get(node, []):
        if neighbor not in current_path:
            stats['generated'] += 1
            res = dls_count_generated(graph, neighbor, goal, depth_limit - 1, current_path, stats)
            if res is not None:
                return res

    return None

def ids_with_node_counts(graph, start, goal, max_depth=10):
    total_generated = 0
    total_expanded = 0
    iteration_records = []

    for depth in range(max_depth + 1):
        stats = {'expanded': 0, 'generated': 1}
        path = dls_count_generated(graph, start, goal, depth, [], stats)

        total_generated += stats['generated']
        total_expanded += stats['expanded']

        iteration_records.append({
            'depth_limit': depth,
            'expanded': stats['expanded'],
            'generated': stats['generated'],
            'found': path is not None
        })

        if path is not None:
            return {
                'path': path,
                'total_generated': total_generated,
                'total_expanded': total_expanded,
                'iterations': iteration_records
            }

    return {
        'path': None,
        'total_generated': total_generated,
        'total_expanded': total_expanded,
        'iterations': iteration_records
    }

def theoretical_ids_nodes(b, d):
    total = 0
    for i in range(d + 1):
        total += (d - i + 1) * (b**i)
    return total

if __name__ == '__main__':
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F', 'G'],
        'D': ['H', 'I'],
        'E': ['J'],
        'F': [],
        'G': [],
        'H': [],
        'I': [],
        'J': []
    }

    start_node = 'A'
    goal_node = 'J'

    res = ids_with_node_counts(graph, start_node, goal_node, max_depth=5)

    for it in res['iterations']:
        print(f"Depth {it['depth_limit']}: Expanded = {it['expanded']}, Generated = {it['generated']}, Found = {it['found']}")

    print("Path Found                :", ' -> '.join(res['path']) if res['path'] else 'None')
    print("Total Nodes Expanded (IDS):", res['total_expanded'])
    print("Total Nodes Generated(IDS):", res['total_generated'])
    print("Theoretical Generated (b=2, d=3):", theoretical_ids_nodes(2, 3))
