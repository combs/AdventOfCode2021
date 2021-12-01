with open("data1.txt", "r") as fh:
    data = list(fh.readlines())

ints = [int(datum.strip()) for datum in data]

results = [ints[i+1] > ints[i] for i in range(len(ints)-1)]

increases = results.count(True)
print(increases)