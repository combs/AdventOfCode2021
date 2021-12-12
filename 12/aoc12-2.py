import networkx

for line in open("data.txt", "r").readlines():
    connections.append( line.strip().split("-"))

mastergraph = networkx.Graph(connections)

for node in mastergraph.nodes:
    mastergraph.nodes[node]['allowed_visits'] = 1
    if node.isupper():
        mastergraph.nodes[node]['allowed_visits'] += len(mastergraph.nodes) 
        # specific val not that significant

def iterate_within(graph, path_so_far, branch):
    solutions = []
    # print("iterating within", path_so_far, "to path", branch, "options:", graph.adj[branch])
    for node in graph.adj[branch]:
        new_path = list(path_so_far) + [branch]
        # print("New_path", new_path)
        if node=="end":
            solutions += [ new_path ]
        elif graph.nodes[node]['allowed_visits'] > path_so_far.count(node):
            solutions += (iterate_within(graph, new_path, node)) 
    return solutions

solutions = []

for node in mastergraph.nodes:
    if mastergraph.nodes[node]['allowed_visits'] == 1 and node not in ['start', 'end']:
        graph = mastergraph.copy()
        graph.nodes[node]['allowed_visits'] += 1
        print(graph.nodes.data('allowed_visits'))

        for branch in graph.adj['start']:
            solutions += iterate_within(graph, ['start'], branch)

solutions_unique = set ( tuple(i) for i in solutions ) 

# print(solutions_unique)

print(len(solutions_unique))