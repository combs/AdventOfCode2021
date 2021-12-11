import numpy

with open("data.txt", "r") as fh:
    lines = fh.readlines()

heightmap = []
for line in lines:
    row = [ int(i) for i in line.strip() ] 
    heightmap.append(row)

heightmap = numpy.array(heightmap)
flashed = numpy.zeros(heightmap.shape)

def get_neighbors(matrix, x, y):
    neighbors = []
    
    for thisX in [x - 1, x, x + 1]:
        for thisY in [y - 1, y, y + 1]:
            if thisX >= 0 and thisX < matrix.shape[1]:
                if thisY >= 0 and thisY < matrix.shape[0]:
                    neighbors.append((thisX, thisY))
    return neighbors

steps = 100
flashes = 0

for step in range(steps):

    # Increment everything by one
    heightmap += 1

    incrementers = []

    for y in range(heightmap.shape[0]):
        for x in range(heightmap.shape[1]):
            if heightmap[y][x] > 9:
                if flashed[y][x] == 0:
                    incrementers.extend(get_neighbors(heightmap, x, y))
                    flashed[y][x] = 1
                    flashes += 1
            
            while len(incrementers) > 0:
                iX, iY = incrementers.pop(0) # Get first 
                heightmap[iY][iX] += 1
                if heightmap[iY][iX] > 9:

                    if flashed[iY][iX] == 0:
                        incrementers.extend(get_neighbors(heightmap, iX, iY))
                        flashed[iY][iX] = 1
                        flashes += 1
    
    flashed.fill(0)
    heightmap[numpy.where(heightmap > 9)] = 0
    # print("Iteration",step)
    # print(heightmap)

print(flashes)



