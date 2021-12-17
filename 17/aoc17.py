

# target area: x=20..30, y=-10..-5

import re
from tqdm import tqdm

with open("data.sample.txt", "r") as fh:
    line = fh.read().strip().split(": ")[1]
    expression = r".*x=(-?[0-9]+)\.\.(-?[0-9]+), y=(-?[0-9]+)\.\.(-?[0-9]+).*"
    print(expression, line)
    matched = re.match(expression, line).groups()
    zone = [int(i) for i in matched]
    # ((int(matched[0]), int(matched[1]), (int(matched[2]), int(matched[3])))


max_y = 0

def is_good(x, y):
    return ( zone[0] <= x <= zone[1]) and (zone[2] <= y <= zone[3])

multiplier = 20
x_range = (0, zone[1] * multiplier)
y_range = (zone[2], abs(zone[2]) * multiplier)

goods = []

for xv in tqdm(range(*x_range)):
    # print("xvelocity",xvelocity)
    for yv in range(*y_range):
        xvelocity, yvelocity = xv, yv 
        # So if you change these in place it confuses the range operator? Whut?
        x, y, my_max_y = 0, 0, 0
        good = False
        while y >= zone[2]:
            good = good or is_good(x, y)
            x += xvelocity
            y += yvelocity
            if xvelocity < 0:
                xvelocity += 1
            elif xvelocity > 0:
                xvelocity -= 1
            yvelocity -= 1

            my_max_y = max(my_max_y, y)

            if xvelocity==0 and (x < zone[0] or x > zone[1]):
                # will never reach desired X
                break
            if xvelocity > 0 and x > zone[1]:
                # overshoot
                break

        if good:
            goods.append((xv, yv))
        if good and my_max_y > max_y:
            max_y = max(my_max_y, y)
            print("successful trajectory: vel", xv, yv, " reached y",my_max_y,"record height now",max_y)
            

print(len(goods), "valid solutions")