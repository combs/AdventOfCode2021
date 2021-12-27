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

    # attempt(str(15111111111111))

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
    cdef long long w, x, y, z, D01, D02, D03, D04, D05, D06, D07, D08, D09, D10, D11, D12, D13, D14
    cdef int input_pos

    input_pos = 0
    w, x, y, z = 0, 0, 0, 0
    w = int(number[input_pos])
    input_pos += 1 

    D01 = int(number[0])
    D02 = int(number[1])
    D03 = int(number[2])
    D04 = int(number[3])
    D05 = int(number[4])
    D06 = int(number[5])
    D07 = int(number[6])
    D08 = int(number[7])
    D09 = int(number[8])
    D10 = int(number[9])
    D11 = int(number[10])
    D12 = int(number[11])
    D13 = int(number[12])
    D14 = int(number[13])
    
    # w is first digit of input.

    # x = 0
    # x = x + z
    # x = x % 26
    # z = int(z / 1)

    # above lines do nothing

    # print(w, x, y, z)
    x = x + 10
    # 
    # is first digit 10? Never possible
    # x = x == w
    # # if not...
    # x = x == 0
    # x is now 1 if first digit was not 10

    
    x = 1 # REWRITE

    # y = 0
    # y = y + 25
    # # set y to 26 or 1
    # y = y * x
    # y = y + 1
    # # z is still 0, so this does nothing
    # z = z * y
    # y = 0

    # y is now 0
    # w, x, y, z:
    # 9  1  0  0

    # set y to DIGIT01 + 12
    # y = y + w
    # y = y + 12
    # x is still 1
    # y = y * x
    # z is 0
    # z = z + y

    z = y = w + 12 # REWRITTEN

    w = int(number[input_pos])
    input_pos += 1 

    # w,    x,    y,    z
    # D02   1    D01+12 D01+12
    # print (w, x, y, z)
    
    # # x = 0
    # # x = x + z
    # # # no way this could ever hit 26
    # # x = x % 26

    # x = z # RW

    # # z = int(z / 1)

    # x = x + 10

    # # w,    x,    y,    z
    # # D02  D01+22 D01+12 D01+12

    # # Is digit 01 + 12 + 10 the same as the new digit? Spoiler: no
    # x = x == w
    # x = x == 0

    # w,    x,    y,    z
    # D02   1    D01+12 D01+12

    # y = 0
    # y = y + 25
    # y = y * x
    # y = y + 1
    # y is 26

    y = 26 # RW

    z = z * y
    # z is 26 * (D01+12)
    
    # D02, 1, 26, 26*(D01+12)
    # print (w, x, y, z)
    # print ("summarized", D02, 1, 26, 26*(D01+12))
    
    # y = 0
    # y = y + w
    # y = y + 10
    # # x is still 1
    # y = y * x

    y = w + 10 # RW

    # w,   x,    y,   z
    # D02, 1, D02+10, 26*(D01+12)

    # print(w,x,y,z)
    z = z + y
    w = int(number[input_pos])
    input_pos += 1 

    # w,   x,   y,     z
    # D03, 1, D02+10, D02+10+(26*(D01+12))

    # print(w,x,y,z)
    # print("summarized2", D03, 1, D02+10, D02+10+(26*(D01+12)))

    # x = 0
    # x = x + z
    # x = x % 26

    w, x, y, z = D03, 1, D02+10, D02+10+(26*(D01+12))
    input_pos = 3

    x = z % 26 # RW

    
    # z = int(z / 1)

    # w,   x,                       y,      z
    # D03, (D02+10+(26*(D01+12)))%26, D02+10, D02+10+(26*(D01+12))
    
    x = x + 12
    
    # D03, (D02+10+(26*(D01+12)))%26 + 12, D02+10, D02+10+(26*(D01+12))

    
    # print (w, x, y, z)
    # print ("summarized3", D03, (D02+10+(26*(D01+12)))%26 + 12, D02+10, D02+10+(26*(D01+12)))

    w, x, y, z = D03, (D02+10+(26*(D01+12)))%26 + 12, D02+10, D02+10+(26*(D01+12))

    x = x == w
    x = x == 0

    # X is now 0 if D03 == (D02+10+(26*D01+12))%26 + 12
    # X is 1 otherwise

    y = 0
    y = y + 25
    y = y * x
    y = y + 1
    # Y is 26 or 1 depending on X

    z = z * y
    # 
    # y = 0
    # y = y + w
    # y = y + 8
    
    y = w + 8 # RW

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
    # x = 0
    # x = x + z
    # x = x % 26

    x = z % 26
    
    z = int(z / 26)
    # z is multiples of 26 

    x = x + -12
    x = x == w
    
    # does the last input digit equal the remainder of [previous z] / 26?

    x = x == 0
    # invert x, so previous True is now 0

    y = 0
    y = y + 25

    y = y * x
    y = y + 1
    # y is 26 if previous was false, else 1
    
    z = z * y
    y = 0
    y = y + w
    y = y + 9
    y = y * x
    z = z + y


    return z
