import sys
import random
import math
import mcSearch

"""
player 1 is x, player 0 is o, turn is t
0btxxxxxxxxx...xo...ooooooooo
"""

turnConstant = 0b1000000000000000000000000000000000000000000000000000000000000000000000000000000000000
def getTurn(board):
    return (board & turnConstant) >> 84

def flipTurn(board):
    return board ^ turnConstant

def printBoard(board):
    print(bin(board))
    sys.stdout.write("\n")
    sys.stdout.write("\n | ")
    t = 0
    mask = 1
    while mask < 2**42:
        t += 1
        if board & mask == mask:
            sys.stdout.write("o | ")
        elif ((board & (mask << 42)) == (mask << 42)):
            sys.stdout.write("x | ")
        else:
            #sys.stdout.write(str(t-1)+" | ")
            sys.stdout.write(". | ")
        mask = mask * 2
        if ((t % 7 == 0) & (t < 42)):
            sys.stdout.write("\n | ")
    sys.stdout.write("\n")
    sys.stdout.write("\n")
    if getTurn(board) == 1:
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

    colOne = 0b100000010000001000000100000010000001
    colTwo = 0b1000000100000010000001000000100000010
    colThree = 0b10000001000000100000010000001000000100
    colFour = 0b100000010000001000000100000010000001000
    colFive = 0b1000000100000010000001000000100000010000
    colSix = 0b10000001000000100000010000001000000100000
    colSeven = 0b100000010000001000000100000010000001000000

    os = board & 0b111111111111111111111111111111111111111111
    xs = (board & 0b111111111111111111111111111111111111111111000000000000000000000000000000000000000000) >> 42
    occupied = os | xs

    moves.append((colOne ^ (occupied & colOne)).bit_length() - 1)
    moves.append((colTwo ^ (occupied & colTwo)).bit_length() - 1)
    moves.append((colThree ^ (occupied & colThree)).bit_length() - 1)
    moves.append((colFour ^ (occupied & colFour)).bit_length() - 1)
    moves.append((colFive ^ (occupied & colFive)).bit_length() - 1)
    moves.append((colSix ^ (occupied & colSix)).bit_length() - 1)
    moves.append((colSeven ^ (occupied & colSeven)).bit_length() - 1)

    print(moves)

    #printMoves(moves)
    return moves


def printMoves(moves):
    for i in range(0, len(moves)):
        printMove(moves[i])

def printMove(m):
    printBoard(1 << m)

def makeLegalMoveByIndex(board, n):
    n = 1 << n
    if getTurn(board) == 1:
        board = board | (n << 42)
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
    board = 0
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
                #board = makeLegalMoveByIndex(board,
                #mcSearch.getAIMove(5000, board, getTurn, getLegalMoves, checkForEndByTurn, makeLegalMoveByIndex))
                break
            try:
                move = int(m)
                if move in moves:
                    board = makeLegalMoveByIndex(board, move)
                    break
            except ValueError:
                print("please enter a number or 'go'")

standalone()



board = 0b1110000000000000000000000000000000000000000000000000000000000000000000000000000000000
printBoard(board)
moves = getLegalMoves(board)
print(moves)

board = makeLegalMoveByIndex(board, moves[0])
printBoard(board)
