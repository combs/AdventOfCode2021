import statistics, numpy

with open("data.txt", "r") as fh:
    dataline = fh.read()
    positions = dataline.strip().split(",")
    positions = numpy.array([int(a) for a in positions], dtype=numpy.int)

# Spoiler alert: It's the median. I double check with other methods too:
# median, mean, mode(s), then iterating through Every Value, because we can

guesses = [statistics.median(positions), statistics.mean(positions)]
guesses.extend(statistics.multimode(positions))
guesses = [ round(a) for a in guesses ]
guesses.extend(list(range(min(positions),max(positions)+1)))

fuels = {}
left, right = min(positions), max(positions)
diff = (right - left)
costs = [0] * (diff + 1)

for i in range(diff + 1):
    costs[i] = i
    if i > 1:
        costs[i] += costs[i-1] 

for position in guesses:
    allpositions = positions.copy()
    allpositions -= position
    allpositions = numpy.absolute(allpositions)

    allcosts = [ costs[position] for position in allpositions]
    totalcost = numpy.sum(allcosts)
    fuels[position] = totalcost
    
best = min(fuels, key=fuels.get)
print("Best position", best, "with fuel expenditure", fuels[best])