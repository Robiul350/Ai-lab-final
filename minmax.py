import math


def minimax(cur_depth: int, node_index: int, is_max: bool, scores: list[int], target_depth: int) -> int:
    """
    Minimax algorithm implementation for a complete binary game tree.
    Reference: https://www.geeksforgeeks.org/dsa/minimax-algorithm-in-game-theory-set-1-introduction/

    :param cur_depth: Current depth in the game tree (starts at 0)
    :param node_index: Index of the current node in the scores array
    :param is_max: True if current turn is Maximizer, False for Minimizer
    :param scores: Array of leaf node evaluation scores
    :param target_depth: Maximum depth (height) of the game tree = log2(len(scores))
    :return: The optimal value determined by Minimax
    """
    # Base case: target depth (leaf node) reached
    if cur_depth == target_depth:
        return scores[node_index]

    if is_max:
        # Maximizer's turn: choose the maximum of left and right child nodes
        left = minimax(cur_depth + 1, node_index * 2, False, scores, target_depth)
        right = minimax(cur_depth + 1, node_index * 2 + 1, False, scores, target_depth)
        return max(left, right)
    else:
        # Minimizer's turn: choose the minimum of left and right child nodes
        left = minimax(cur_depth + 1, node_index * 2, True, scores, target_depth)
        right = minimax(cur_depth + 1, node_index * 2 + 1, True, scores, target_depth)
        return min(left, right)


def minimax_with_path(
    cur_depth: int,
    node_index: int,
    is_max: bool,
    scores: list[int],
    target_depth: int
) -> tuple[int, list[dict]]:
    """
    Minimax evaluation that also returns the optimal decision path from root to leaf.

    :return: (optimal_value, list_of_step_descriptions)
    """
    # Base case: target depth reached
    if cur_depth == target_depth:
        leaf_val = scores[node_index]
        return leaf_val, [{
            'depth': cur_depth,
            'role': 'LEAF',
            'node_index': node_index,
            'action': f"Terminal leaf node at index {node_index}",
            'value': leaf_val
        }]

    if is_max:
        left_val, left_path = minimax_with_path(cur_depth + 1, node_index * 2, False, scores, target_depth)
        right_val, right_path = minimax_with_path(cur_depth + 1, node_index * 2 + 1, False, scores, target_depth)

        if left_val >= right_val:
            chosen_action = f"MAX chooses Left child (val {left_val} >= {right_val})"
            step = {
                'depth': cur_depth,
                'role': 'MAX',
                'node_index': node_index,
                'action': chosen_action,
                'value': left_val
            }
            return left_val, [step] + left_path
        else:
            chosen_action = f"MAX chooses Right child (val {right_val} > {left_val})"
            step = {
                'depth': cur_depth,
                'role': 'MAX',
                'node_index': node_index,
                'action': chosen_action,
                'value': right_val
            }
            return right_val, [step] + right_path
    else:
        left_val, left_path = minimax_with_path(cur_depth + 1, node_index * 2, True, scores, target_depth)
        right_val, right_path = minimax_with_path(cur_depth + 1, node_index * 2 + 1, True, scores, target_depth)

        if left_val <= right_val:
            chosen_action = f"MIN chooses Left child (val {left_val} <= {right_val})"
            step = {
                'depth': cur_depth,
                'role': 'MIN',
                'node_index': node_index,
                'action': chosen_action,
                'value': left_val
            }
            return left_val, [step] + left_path
        else:
            chosen_action = f"MIN chooses Right child (val {right_val} < {left_val})"
            step = {
                'depth': cur_depth,
                'role': 'MIN',
                'node_index': node_index,
                'action': chosen_action,
                'value': right_val
            }
            return right_val, [step] + right_path


def find_optimal_value(scores: list[int], is_max: bool = True) -> int:
    """
    Helper function to calculate tree depth and run minimax.
    """
    if not scores:
        raise ValueError("Scores array cannot be empty.")

    # Check if length is a power of 2 for a complete binary tree
    n = len(scores)
    if (n & (n - 1)) != 0:
        raise ValueError("Number of leaf nodes must be a power of 2 for a full binary tree.")

    tree_depth = int(math.log2(n))
    return minimax(0, 0, is_max, scores, tree_depth)


if __name__ == '__main__':
    scores = [3, 5, 2, 9, 12, 5, 23, 23]
    tree_depth = int(math.log2(len(scores)))

    print("=" * 60)
    print("MINIMAX ALGORITHM TRACE")
    print("=" * 60)
    print(f"Leaf Node Scores : {scores}")
    print(f"Total Leaves     : {len(scores)}")
    print(f"Tree Depth       : {tree_depth}\n")

    optimal_val, path = minimax_with_path(0, 0, True, scores, tree_depth)
    print(f"Optimal Value for Maximizer: {optimal_val}\n")

    print("Optimal Path Breakdown:")
    for step in path:
        print(f"  [Depth {step['depth']}] ({step['role']}): {step['action']} -> Resulting Value: {step['value']}")
