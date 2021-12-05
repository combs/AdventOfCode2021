import numpy

biggestx = biggesty = 0
lines = []

def explodePoints(p1, p2):
    points = []
    (x1, y1), (x2, y2) = p1, p2
    xdiff, ydiff = x1 - x2, y1 - y2
    steps = max(abs(xdiff), abs(ydiff))
    xstep, ystep = float(xdiff) / float(steps), float(ydiff) / float(steps)

    for step in range(steps + 1):
        points.append( (int(x1 - (xstep * step)), int(y1 - (ystep * step))))
    
    return points

def isDiagonal(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    return (x1 - x2 != 0) and (y1 - y2 != 0)

with open("data.txt", "r") as fh:
    for dataline in fh.readlines():
        halves = dataline.split(" -> ")
        halves = [ i.split(",") for i in halves ] 
        linepoints = [ (int(i[0]), int(i[1])) for i in halves ]
        ((x1, y1), (x2, y2)) = linepoints
        biggestx, biggesty = max(x1, x2, biggestx), max(y1, y2, biggesty)
        lines.append(linepoints)

board = numpy.zeros((biggesty + 1, biggestx + 1), dtype=numpy.int)

for linepoints in lines:
    points = explodePoints(*linepoints)
    for (x, y) in points:
        board[y][x] += 1

print(numpy.count_nonzero(board > 1))