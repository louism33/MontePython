import sys
import random
import math
import mcSearch

"""
player 1 is x, player 0 is o
0btxxxxxxxxxooooooooo
"""

turnConstant = 0b1000000000000000000
def getTurn(board):
    return (board & turnConstant) >> 18

def flipTurn(board):
    return board ^ turnConstant

def printBoard(n):
    print(bin(n))
    sys.stdout.write("\n")
    sys.stdout.write("\n | ")
    t = 0
    mask = 1
    while mask < 2**9:
        t += 1
        if n & mask == mask:
            sys.stdout.write("o | ")
        elif ((n & (mask << 9)) == (mask << 9)):
            sys.stdout.write("x | ")
        else:
            #sys.stdout.write(str(t-1)+" | ")
            sys.stdout.write(". | ")
        mask = mask * 2
        if ((t % 3 == 0) & (t < 8)):
            sys.stdout.write("\n | ")
    sys.stdout.write("\n")
    sys.stdout.write("\n")
    if getTurn(n) == 1:
        sys.stdout.write("It is x's turn")
    else:
        sys.stdout.write("It is o's turn")
    sys.stdout.write("\n")
    sys.stdout.write("\n")

def getLegalMoves(board):
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

def makeLegalMoveByIndex(board, n):
    moves = getLegalMoves(board)
    if n in moves:
        n = 2 ** n
        if getTurn(board) == 1:
            board = board | (n << 9)
        else:
            board = board | n
    return flipTurn(board)


def checkForEndByTurn(board, moves, player): # player 0 is o
    rowOne = 0b111
    rowTwo = 0b111000
    rowThree = 0b111000000

    colOne = 0b1001001
    colTwo = 0b10010010
    colThree = 0b100100100

    diag = 0b100010001
    antiDiag = 0b1010100

    if player == 1:
        board = board >> 9
    if rowOne & board == rowOne:
        return 1
    if rowTwo & board == rowTwo:
        return 1
    if rowThree & board == rowThree:
        return 1

    if colOne & board == colOne:
        return 1
    if colTwo & board == colTwo:
        return 1
    if colThree & board == colThree:
        return 1

    if diag & board == diag:
        return 1
    if antiDiag & board == antiDiag:
        return 1

    if len(moves) == 0:
        return 0.5

    return None

def standalone():
    board = 0b1000000000000000000
    while True:
        printBoard(board)
        moves = getLegalMoves(board)
        player = getTurn(board)
        result = checkForEndByTurn(board, moves, 1-player)
        if result != None:
            if result == 1:
                if player == 1:
                    print("win for o")
                else:
                    print("win for x")
            else:
                print("draw")
            return result
        while True:
            m = input("input a number for your move, or 'go' for an ai move\n")
            if m == "go":
                board = makeLegalMoveByIndex(board,
                mcSearch.getAIMove(5000, board, getTurn, getLegalMoves, checkForEndByTurn, makeLegalMoveByIndex))
                break
            try:
                move = int(m)
                if move in moves:
                    board = makeLegalMoveByIndex(board, move)
                    break
            except ValueError:
                print("please enter a number or 'go'")

standalone()
