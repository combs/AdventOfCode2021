import networkx
from networkx.classes.function import path_weight

with open("data.sample.txt", "r") as fh:
    inputs = [i.strip() for i in fh.readlines()]

height, width = len(inputs),len(inputs[0])
repeats = (5, 5)
graph = networkx.generators.lattice.grid_2d_graph(width * repeats[0],height * repeats[1]).to_directed()

for metax in range(repeats[0]):
    for metay in range(repeats[1]):
        metaval = metax + metay
        for x in range(width):
            for y in range(height):
                newx = x + (metax * width)
                newy = y + (metay * height)
                for succ in graph.successors((newx, newy)):
                    val = (int(inputs[y][x])) + metaval
                    
                    while val > 9:
                        val -= 9
                    graph.edges[(newx, newy),succ]["weight"] = val

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

path = networkx.shortest_path(graph, source=(0,0), target=((repeats[0] * width) - 1,(repeats[1] * height) - 1), weight="weight")

for y in range(repeats[1] * height):
    for x in range(repeats[1] * width ):
        for succ in graph.successors((x, y)):
            if (x, y) in path:
                print(color.BOLD, end="")

            print(graph.edges[(x,y),succ]["weight"], end="")
            if (x, y) in path:
                print(color.END, end="")
                
            break
    print(" ")


nx_weight = path_weight(graph, path, "weight")
print(len(path), " hops, weight:", nx_weight)

