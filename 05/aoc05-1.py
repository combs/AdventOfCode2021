import numpy

biggestx = biggesty = 0
lines = []

def explodePoints(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    xdiff, ydiff = x1 - x2, y1 - y2
    
    steps = max(abs(xdiff),abs(ydiff))

    xstep = float(xdiff) / float(steps)
    ystep = float(ydiff) / float(steps)

    points = []

    for step in range(steps + 1):
        points.append( (int(x1 - (xstep * step)), int(y1 - (ystep * step))))
    
    return points

def isDiagonal(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    
    if x1 - x2 == 0 or y1 - y2 == 0:
        return False
    return True


with open("data.txt", "r") as fh:

    for dataline in fh.readlines():
        halves = dataline.split(" -> ")
        halves = [ i.split(",") for i in halves ] 

        linepoints = [ (int(i[0]), int(i[1])) for i in halves ]
        ((x1, y1), (x2, y2)) = linepoints
        biggestx = max(x1, x2, biggestx)
        biggesty = max(y1, y2, biggesty)
        # print(x1, y1, x2, y2)
        lines.append(linepoints)

board = numpy.zeros( (biggesty + 1, biggestx + 1), dtype=numpy.int)

for linepoints in lines:
    if isDiagonal(*linepoints):
        print("line was diagonal, ignored:", linepoints)
        continue

    points = explodePoints(*linepoints)
    print("for line",linepoints,"got points",points)


    for (x, y) in points:
        board[y][x] += 1
    
print(board)
print(numpy.count_nonzero(board > 1))
