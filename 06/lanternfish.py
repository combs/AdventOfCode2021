
import numpy
from tqdm import tqdm

def gofish(iterations):
    with open("data.txt", "r") as fh:
        dataline = fh.read()
        starting = dataline.strip().split(",")
        starting = [int(a) for a in starting]

    ages = {}
    for i in range(0, 9):
        ages[i] = starting.count(i)

    for day in tqdm(range(iterations), desc="Fish stuff..."):
        newages = {}
        for i in ages.keys():
            if i > 0:
                newages[i-1] = ages[i]
        newages[6] += ages[0]
        newages[8] = ages[0]
        ages = newages
        # print(day,ages)

    print(sum(ages.values()))
