import re, numpy, sys

with open("data.txt", "r") as fh:
    data = list(fh.readlines())

order = data.pop(0).split(",")
order = [int(a) for a in order]
boards = []

while len(data) > 4:
    
    if len(data[0]) < 5:
        data.pop(0)
        continue

    boardraw = data[0:5]
    board = []
    for line in boardraw:
        parsed = re.sub(r' +', ' ', line).strip().split(" ")
        parsed = [int(a) for a in parsed]
        board.append(parsed)

    boards.append(numpy.array(board))


    for i in range(5):
        data.pop(0)
        
# print(boards)

def checkBoard(board, answers):
    rows, cols = board.shape
    for row in range(rows):
        good = True
        for col in range(cols):

            if board[row][col] not in answers:
                good = False
        if good:
            print("bingo row",row)
            return True
            
    for col in range(cols):
        good = True
        for row in range(rows):
            if board[row][col] not in answers:
                good = False
        if good:
            print("bingo col",col)
            return True
    
    # good = True
    # for i in range(rows):
    #     if board[i][i] not in answers:
    #         good = False
    # if good:
    #     print("bingo diagonal UL-LR")
    #     return True

    # good = True
    # for i in range(rows):
    #     if board[(rows - i - 1)][i] not in answers:
    #         good = False
    # if good:
    #     print("bingo diagonal LL-UR")
    #     return True
    
    return False

def undrawn(board, answers):
    flat = board.flatten()
    return [ i for i in flat if i not in answers]

drawn = []
while len(order):
    drawn.append(order.pop(0))
    for board in boards:
        if checkBoard(board, drawn):
            print("BINGO! winning board:")
            print(board)
            print("drawn numbers:", drawn)
            summed = sum(undrawn(board, drawn))
            print ("sum of undrawn numbers:", summed, "final answer:", drawn[-1] * summed)

            sys.exit(0)
