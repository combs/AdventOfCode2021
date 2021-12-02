with open("data.txt", "r") as fh:
    data = list(fh.readlines())

depth, distance = 0, 0

for line in data:
    operation, amount = line.strip().split(" ")

    if operation == "forward": 
        distance += int(amount)

    elif operation == "down":
        depth += int(amount)
        
    elif operation == "up":
        depth -= int(amount)

print(depth * distance)
