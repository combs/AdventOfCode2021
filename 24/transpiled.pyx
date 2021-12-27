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
        remainder = attempt(str(number))

        if remainder == 0:
            # valid
            largest = number
            print("solved",number)
            sys.exit(0)


def attempt(number):
    cdef long long w, x, y, z
    cdef int input_pos

    input_pos = 0
    w, x, y, z = 0, 0, 0, 0
    w = int(number[input_pos])  
    input_pos += 1 
    x = 0
    x = x + z
    x = x % 26
    z = int(z / 1)
    x = x + 10
    x = x == w
    x = x == 0
    y = 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = 0
    y = y + w
    y = y + 12
    y = y * x
    z = z + y
    w = int(number[input_pos])  
    input_pos += 1 
    x = 0
    x = x + z
    x = x % 26
    z = int(z / 1)
    x = x + 10
    x = x == w
    x = x == 0
    y = 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = 0
    y = y + w
    y = y + 10
    y = y * x
    z = z + y
    w = int(number[input_pos])  
    input_pos += 1 
    x = 0
    x = x + z
    x = x % 26
    z = int(z / 1)
    x = x + 12
    x = x == w
    x = x == 0
    y = 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = 0
    y = y + w
    y = y + 8
    y = y * x
    z = z + y
    w = int(number[input_pos])  
    input_pos += 1 
    x = 0
    x = x + z
    x = x % 26
    z = int(z / 1)
    x = x + 11
    x = x == w
    x = x == 0
    y = 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = 0
    y = y + w
    y = y + 4
    y = y * x
    z = z + y
    w = int(number[input_pos])  
    input_pos += 1 
    x = 0
    x = x + z
    x = x % 26
    z = int(z / 26)
    x = x + 0
    x = x == w
    x = x == 0
    y = 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = 0
    y = y + w
    y = y + 3
    y = y * x
    z = z + y
    w = int(number[input_pos])  
    input_pos += 1 
    x = 0
    x = x + z
    x = x % 26
    z = int(z / 1)
    x = x + 15
    x = x == w
    x = x == 0
    y = 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = 0
    y = y + w
    y = y + 10
    y = y * x
    z = z + y
    w = int(number[input_pos])  
    input_pos += 1 
    x = 0
    x = x + z
    x = x % 26
    z = int(z / 1)
    x = x + 13
    x = x == w
    x = x == 0
    y = 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = 0
    y = y + w
    y = y + 6
    y = y * x
    z = z + y
    w = int(number[input_pos])  
    input_pos += 1 
    x = 0
    x = x + z
    x = x % 26
    z = int(z / 26)
    x = x + -12
    x = x == w
    x = x == 0
    y = 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = 0
    y = y + w
    y = y + 13
    y = y * x
    z = z + y
    w = int(number[input_pos])  
    input_pos += 1 
    x = 0
    x = x + z
    x = x % 26
    z = int(z / 26)
    x = x + -15
    x = x == w
    x = x == 0
    y = 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = 0
    y = y + w
    y = y + 8
    y = y * x
    z = z + y
    w = int(number[input_pos])  
    input_pos += 1 
    x = 0
    x = x + z
    x = x % 26
    z = int(z / 26)
    x = x + -15
    x = x == w
    x = x == 0
    y = 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = 0
    y = y + w
    y = y + 1
    y = y * x
    z = z + y
    w = int(number[input_pos])  
    input_pos += 1 
    x = 0
    x = x + z
    x = x % 26
    z = int(z / 26)
    x = x + -4
    x = x == w
    x = x == 0
    y = 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = 0
    y = y + w
    y = y + 7
    y = y * x
    z = z + y
    w = int(number[input_pos])  
    input_pos += 1 
    x = 0
    x = x + z
    x = x % 26
    z = int(z / 1)
    x = x + 10
    x = x == w
    x = x == 0
    y = 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = 0
    y = y + w
    y = y + 6
    y = y * x
    z = z + y
    w = int(number[input_pos])  
    input_pos += 1 
    x = 0
    x = x + z
    x = x % 26
    z = int(z / 26)
    x = x + -5
    x = x == w
    x = x == 0
    y = 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = 0
    y = y + w
    y = y + 9
    y = y * x
    z = z + y
    w = int(number[input_pos])  
    input_pos += 1 
    x = 0
    x = x + z
    x = x % 26
    z = int(z / 26)
    x = x + -12
    x = x == w
    x = x == 0
    y = 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = 0
    y = y + w
    y = y + 9
    y = y * x
    z = z + y


    return z
