
b = 2
d = 3

total_nodes = 0

for depth in range(1, d + 1):

    nodes = 0

    for level in range(1, depth + 1):
        nodes += b ** level

    print("Depth", depth, "=", nodes, "nodes")

    total_nodes += nodes

print("Total nodes =", total_nodes)