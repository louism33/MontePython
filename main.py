# a basic noughts and crosses game in python
import sys
import util.util

#board = 0b0000000000000000000



turnConstant = 0b1000000000000000000
def getTurnBit(board): # x starts
    return (board & turnConstant) == turnConstant
def flipTurn(board):
    return board ^ turnConstant

def printBoard(n):
    sys.stdout.write("\n")
    sys.stdout.write("\n | ")
    t = 0
    mask = 1
    while mask < 2**9:
        #print()
        #print(bin(mask))
        #print()
        t += 1
        if n & mask == mask:
            sys.stdout.write("x | ")
        elif ((n & (mask << 9)) == (mask << 9)):
            sys.stdout.write("o | ")
        else:
            sys.stdout.write(str(t-1)+" | ")
            #sys.stdout.write(". | ")
        mask = mask * 2
        if ((t % 3 == 0) & (t < 8)):
            sys.stdout.write("\n | ")
    sys.stdout.write("\n")
    sys.stdout.write("\n")
    if getTurnBit(board):
        sys.stdout.write("It is o's turn")
    else:
        sys.stdout.write("It is x's turn")
    sys.stdout.write("\n")
    sys.stdout.write("\n")

def getLegalMoves(board): ## can be replaced by xor a mask, then pop count
    moves = []
    mask = 1
    t = 0
    mask = 1
    while mask < 2**9:
        if not((board & mask == mask) | (board & (mask << 9) == (mask << 9))):
            moves.append(t)
        t += 1
        mask = mask * 2
    return moves


def makeLegalMoveSafeIndex(board, n):
    moves = getLegalMoves(board)
    if n in moves:
        n = 2 ** n
        if getTurnBit(board):
            board = board | (n << 9)
        else:
            board = board | n
    return flipTurn(board)

def checkForEnd(board):
    rowOne = 0b111
    rowTwo = 0b111000
    rowThree = 0b111000000

    colOne = 0b1001001
    colTwo = 0b10010010
    colThree = 0b100100100

    diag = 0b100010001
    antiDiag = 0b1010100
    for i in range(-1, 2, 2):
        if i == 1:
            board = board >> 9
        if rowOne & board == rowOne:
            return i
        if rowTwo & board == rowOne:
            return i
        if rowThree & board == rowOne:
            return i

        if colOne & board == rowOne:
            return i
        if colTwo & board == rowOne:
            return i
        if colThree & board == rowOne:
            return i

        if diag & board == rowOne:
            return i
        if antiDiag & board == rowOne:
            return i



board = 0b0000000000000000000
#board = 0b0111
def start():
    global board
    while True:
        printBoard(board)
        moves= getLegalMoves(board)
        if len(moves) == 0:
            print("draw")
            return 0
        #print(moves)
        while True:
            m = input("which move do you want to make? ")
            try:
                move = int(m)
            except ValueError:
                print("please enter a number")
            if move in moves:
                board = makeLegalMoveSafeIndex(board, move)
                result = checkForEnd(board)
                if result == 1:
                    print("win for o")
                    return 1
                if result == -1:
                    print("win for x")
                    return -1
                break


start()
