# cython: language_level=3,infer_types=False

from tqdm import tqdm
import sys

def do_it():
    cdef long long largest 
    cdef long long w, x, y, z
    cdef list input_values

    with open("data.txt", "r") as fh:
        instructions = fh.readlines()

    largest = 0

    # attempt(str(15111111111111))

    number = "94954989425496"
    summed,length = attempt(number)
    print(summed,length,number)
    
    # for digit in range(1,10):
    #     number = [str(digit)] * 14
    #     number = "".join(number)
    #     summed,length = attempt(number)
    #     print(summed,length,number)
    sys.exit(0)

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
    cdef int input_pos, step_number

    input_pos = 0
    w, x, y, z = 0, 0, 0, 0
    stack = [0]

    offsetX = [10, 10, 12, 11, 0, 15, 13, -12, -15, -15, -4, 10, -5, -12]
    offsetY = [12, 10, 8, 4, 3, 10, 6, 13, 8, 1, 7, 6, 9, 9]
    pops = [False, False, False, False, True, False, False, True, True, True, True, False, True, True]

    for input_pos in range(0,14):
        
        digit = int(number[input_pos])
        x = stack[-1] % 26

        if pops[input_pos]:
            stack.pop()

        x += offsetX[input_pos]
        print("digit",input_pos+1,"wanted",x,"got",digit,"stack",stack)
        if x != digit:
            stack.append(digit + offsetY[input_pos])
        
            

    print("number",number,"stack",stack)
    return sum(stack), len(stack)
