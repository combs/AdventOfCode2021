import numpy

with open("data.txt", "r") as fh:
    lines = fh.readlines()

heightmap = []
for line in lines:
    row = [ int(i) for i in line.strip() ] 
    heightmap.append(row)

heightmap = numpy.array(heightmap)

size = (len(heightmap[0])-1,len(heightmap)-1)

localminima = []
localminima_sum = 0

for rowindex, row in enumerate(heightmap):
    for colindex, col in enumerate(row):
        neighbors = []
        good = True
        if rowindex > 0:
            neighbors.append(heightmap[rowindex-1][colindex])
        if rowindex < size[1]:
            neighbors.append(heightmap[rowindex+1][colindex])
        if colindex > 0:
            neighbors.append(heightmap[rowindex][colindex-1])
        if colindex < size[0]:
            neighbors.append(heightmap[rowindex][colindex+1])
        # print("neighbors for",colindex, rowindex, neighbors)
        for neighbor in neighbors:
            if col >= neighbor:
                # print(col,"gte", neighbor)
                good = False
        
        if good:
            localminima.append((colindex, rowindex))
            localminima_sum += (1 + col)

# print(localminima)
print(localminima_sum)
