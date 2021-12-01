with open("data1.txt", "r") as fh:
    data = list(fh.readlines())

ints = [int(datum.strip()) for datum in data]

sums = [sum(ints[i:i+3]) for i in range(len(ints)-2)]
results = [sums[i+1] > sums[i] for i in range(len(sums)-1)]

increases = results.count(True)
print(increases)