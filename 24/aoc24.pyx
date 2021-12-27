# cython: language_level=3,infer_types=False

from tqdm import tqdm
import sys

def do_it():
    cdef long long largest, number
    cdef long long w, x, y, z
    cdef list input_values

    with open("data.txt", "r") as fh:
        instructions = fh.readlines()

    largest = 0

    for number in tqdm(range(100000000000000,11111111111111,-1)):
        if '0' in str(number):
            continue

        w, x, y, z = 0, 0, 0, 0
        input_values = [int(i) for i in str(number)]
        input_pos = 0

        for i in instructions:
            i = i.strip().split(" ")
            # print(i)
            if len(i)==3:
                if i[2]=='w':
                    i[2] = w
                elif i[2]=='x':
                    i[2] = x
                elif i[2]=='y':
                    i[2] = y
                elif i[2]=='z':
                    i[2] = z
                else:
                    i[2] = int(i[2])

            if i[0]=="add":
                
                if i[1]=='w':
                    w += i[2]
                elif i[1]=='x':
                    x += i[2]
                elif i[1]=='y':
                    y += i[2]
                elif i[1]=='z':
                    z += i[2]

            elif i[0]=="mul":
                if i[1]=='w':
                    w *= i[2]
                elif i[1]=='x':
                    x *= i[2]
                elif i[1]=='y':
                    y *= i[2]
                elif i[1]=='z':
                    z *= i[2]

            elif i[0]=="div":
                
                if i[1]=='w':
                    w /= i[2]
                elif i[1]=='x':
                    x /= i[2]
                elif i[1]=='y':
                    y /= i[2]
                elif i[1]=='z':
                    z /= i[2]

            elif i[0]=="mod":
                
                if i[1]=='w':
                    w %= i[2]
                elif i[1]=='x':
                    x %= i[2]
                elif i[1]=='y':
                    y %= i[2]
                elif i[1]=='z':
                    z %= i[2]

            elif i[0]=="eql":
                
                if i[1]=='w':
                    w = 1 if w == i[2] else 0
                elif i[1]=='x':
                    x = 1 if x == i[2] else 0
                elif i[1]=='y':
                    y = 1 if y == i[2] else 0
                elif i[1]=='z':
                    z = 1 if z == i[2] else 0

            elif i[0]=="inp":
                
                if i[1]=='w':
                    w = input_values[input_pos]
                elif i[1]=='x':
                    x = input_values[input_pos]
                elif i[1]=='y':
                    y = input_values[input_pos]
                elif i[1]=='z':
                    z = input_values[input_pos]

                input_pos += 1

        if z == 0:
            # valid
            largest = number
            print("solved",number)
            sys.exit(0)
        

    print(largest)
            


