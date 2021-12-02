with open("data.txt", "r") as fh:
    data = list(fh.readlines())

depth, distance, aim = 0, 0, 0

for line in data:
    operation, amount = line.strip().split(" ")
    amount = int(amount)

    if operation == "forward": 
        distance += amount
        depth += (aim * amount)

    elif operation == "down":
        aim += amount

    elif operation == "up":
        aim -= amount
        
print(depth * distance)
