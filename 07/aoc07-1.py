import statistics, numpy

with open("data.txt", "r") as fh:
    dataline = fh.read()
    positions = dataline.strip().split(",")
    positions = numpy.array([int(a) for a in positions], dtype=numpy.int)

# Spoiler alert: It's the median. I double check with other methods too:
# median, mean, mode(s), then iterating through Every Value, because we can

guesses = [statistics.mean(positions), statistics.median(positions)]
guesses.extend(statistics.multimode(positions))
guesses = [ round(a) for a in guesses ]
guesses.extend(list(range(min(positions),max(positions) + 1)))

fuels = {}

for position in guesses:
    allpositions = positions.copy()
    allpositions -= position
    fuels[position] = numpy.sum(numpy.absolute(allpositions))
    
best = min(fuels, key=fuels.get)
print("Best position", best, "with fuel expenditure", fuels[best])