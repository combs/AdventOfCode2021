import numpy

xaxis = 1
yaxis = 0
board = []

with open("data.txt", "r") as fh:
    for line in fh.readlines():
        row = [ 3 if line[i] == ">" else 0 for i in range(len(line.strip())) ]
        row2 = [ 6 if line[i] == "v" else row[i] for i in range(len(line.strip())) ]
        board.append(row2)
        
starting_board = numpy.array(board, dtype=numpy.int)
# print(starting_board)

def iterate(cukes):

    changed = 0

    horiz = cukes==3
    horiz_dests = numpy.roll(cukes==0, -1, xaxis)
    horiz_movers = horiz_dests & horiz
    changed += numpy.count_nonzero(horiz_movers)

    cukes[horiz_movers] = 0
    cukes[numpy.roll(horiz_movers, 1, xaxis)] = 3

    vert = cukes==6
    vert_dests = numpy.roll(cukes==0, -1, yaxis)
    vert_movers = vert_dests & vert
    changed += numpy.count_nonzero(vert_movers)

    cukes[vert_movers] = 0
    cukes[numpy.roll(vert_movers, 1, yaxis)] = 6

    return cukes, changed

changed = None
board = starting_board.copy()

iterations = 0
while changed != 0:
    board, changed = iterate(board)
    iterations += 1
    # print(changed)

print("iterations",iterations)



