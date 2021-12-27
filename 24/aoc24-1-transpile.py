import pyximport
pyximport.install()

from tqdm import tqdm

with open("data.txt", "r") as fh:
    instructions = fh.readlines()

largest = 0

head = open("header", "r").read()
tail = open("footer", "r").read()

code = head 


for i in instructions:
    i = i.strip().split(" ")
    code += "    "
    # print(i)
    if i[0]=="add":
        code += i[1] + " = " + i[1] + " + " + i[2]
    elif i[0]=="mul":
        if i[2] == "0":
            code += i[1] + " = 0"
        else:
            code += i[1] + " = " + i[1] + " * " + i[2]
    elif i[0]=="div":
        code += i[1] + " = int(" + i[1] + " / " + i[2] + ")"
    elif i[0]=="mod":
        code += i[1] + " = " + i[1] + " % " + i[2]
    elif i[0]=="eql":
        code += i[1] + " = " + i[1] + " == " + i[2]
        
    elif i[0]=="inp":
        code += i[1] + " = int(number[input_pos])  \n    input_pos += 1 " 
    code += "\n"        

code += tail
output = open("transpiled.pyx", "w").write(code)
