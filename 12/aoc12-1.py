import networkx

for line in open("data.txt", "r").readlines():
    connections.append( line.strip().split("-"))

graph = networkx.Graph(connections)

for node in graph.nodes:
    graph.nodes[node]['allowed_visits'] = 1
    if node.isupper(): # uppercase = big cave
        graph.nodes[node]['allowed_visits'] += len(graph.nodes) 
        # specific val not that significant

def iterate_within(path_so_far, branch):
    solutions = []
    # print("iterating within", path_so_far, "to path", branch, "options:", graph.adj[branch])
    for node in graph.adj[branch]:
        new_path = list(path_so_far) + [branch]
        # print("New_path", new_path)
        if node=="end":
            solutions += [ new_path ]
        elif graph.nodes[node]['allowed_visits'] > path_so_far.count(node):
            solutions += (iterate_within(new_path, node)) 
    return solutions

solutions = []
for branch in graph.adj['start']:

    solutions += iterate_within(['start'], branch)

# print(solutions)

print(len(solutions))