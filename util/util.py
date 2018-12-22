import sys


def getTurn(board):
    return bin(board).count("1") % 2 == 0

def printBoard(n):
    sys.stdout.write("\n")
    sys.stdout.write("\n | ")
    t = 0
    mask = 2
    while mask <= 2**9:
        t += 1
        if n & mask == mask:
            sys.stdout.write("x | ")
        elif n & (mask << 9) == (mask << 9):
            sys.stdout.write("o | ")
        else:
            sys.stdout.write(". | ")
        mask = mask * 2
        if ((t % 3 == 0) & (t < 8)):
            sys.stdout.write("\n | ")
    sys.stdout.write("\n")
    sys.stdout.write("\n")
    if getTurn(board):
        sys.stdout.write("It is o's turn")
    else:
        sys.stdout.write("It is x's turn")
    sys.stdout.write("\n")
    sys.stdout.write("\n")

def getLegalMoves(board):
    moves = []
    mask = 1
    t = 0
    mask = 1
    while mask < 2**9:
        t += 1
        if board & mask == 0:
            moves.append(mask)
        mask = mask * 2
    return moves
