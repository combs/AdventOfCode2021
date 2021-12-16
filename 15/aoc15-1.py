import networkx
from networkx.classes.function import path_weight

with open("data.txt", "r") as fh:
    inputs = [i.strip() for i in fh.readlines()]

height, width = len(inputs),len(inputs[0])
graph = networkx.generators.lattice.grid_2d_graph(width,height).to_directed()

for x in range(width):
    for y in range(height):
        for pred in graph.predecessors((x,y)):
            graph.edges[pred,(x,y)]["weight"] = int(inputs[y][x])

path = networkx.shortest_path(graph, source=(0,0), target=(width-1,height-1), weight="weight")
nx_weight = path_weight(graph, path, "weight")
print(len(path), " hops:", path, "weight:", nx_weight)
