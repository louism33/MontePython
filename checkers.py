import sys
import random
import math
import mcSearch

"""
player 1 is x, player 0 is o, turn is t
0btxxxxxxxxx...xo...ooooooooo
"""

turnConstant = 0b100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
def getTurn(board):
    return (board & turnConstant) >> 128

def flipTurn(board):
    return board ^ turnConstant

def printBoard(board):
    print(bin(board))
    sys.stdout.write("\n")
    sys.stdout.write("\n | ")
    t = 0
    mask = 1
    while mask < 2**64:
        t += 1
        if board & mask == mask:
            sys.stdout.write("o | ")
        elif ((board & (mask << 64)) == (mask << 64)):
            sys.stdout.write("x | ")
        else:
            if (((t + ((t-1) // 8)) % 2) == 1):
                sys.stdout.write("  | ")
            else:
                sys.stdout.write(". | ")
        mask = mask * 2
        if ((t % 8 == 0) & (t < 64)):
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
    global columns
    moves = []
    os = board & 0b111111111111111111111111111111111111111111
    xs = (board & 0b111111111111111111111111111111111111111111000000000000000000000000000000000000000000) >> 42
    occupied = os | xs
    for i in range(0, len(columns)):
        if ((columns[i] & occupied) == columns[i]):
            continue
        moves.append(i)
    return moves

def printMoves(moves):
    for i in range(0, len(moves)):
        printMove(moves[i])

def printMove(m):
    printBoard(1 << m)

def makeLegalMoveByIndex(board, colNum):
    global columns
    os = board & 0b111111111111111111111111111111111111111111
    xs = (board & 0b111111111111111111111111111111111111111111000000000000000000000000000000000000000000) >> 42
    occupied = os | xs
    squareToPlayIndex = ((columns[colNum] ^ (occupied & columns[colNum])).bit_length() - 1)
    squareToPlay = 1 << squareToPlayIndex
    if getTurn(board) == 1:
        board = board | (squareToPlay << 42)
    else:
        board = board | squareToPlay
    return flipTurn(board)

def checkForEndByTurn(board, moves, player): # player 0 is o
    if player == 1:
        board = board >> 42

    if len(moves) == 0:
        return 0.5

    horizontalFour = 0b1111
    for row in range(0, 6):
        for i in range(0, 4):
            mask = (horizontalFour << i) << (row * 7)
            if mask & board == mask:
                return 1

    verticalFour = 0b1000000100000010000001
    for row in range(0, 7):
        for i in range(0, 3):
            mask = (verticalFour << (i*7)) << (row)
            if mask & board == mask:
                return 1

    diag = 0b1000000010000000100000001
    antiDiag = 0b1000001000001000001000
    for row in range(0, 4):
        for i in range(0, 3):
            maskD = (diag << (i*7)) << (row)
            maskAD = (antiDiag << (i*7)) << (row)
            if maskD & board == maskD:
                return 1
            if maskAD & board == maskAD:
                return 1

    return None

def standalone():
    board = 0
    while True:
        printBoard(board)
        moves = getLegalMoves(board)
        player = getTurn(board)
        result = checkForEndByTurn(board, moves, 1 - player)
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
            print(moves)
            m = input("input a number for your move, or 'go' for an ai move\n")
            if m == "go":
                board = makeLegalMoveByIndex(board,
                mcSearch.getAIMove(20000, board, getTurn, getLegalMoves, checkForEndByTurn, makeLegalMoveByIndex))
                break
            try:
                move = int(m)
                if move in moves:
                    board = makeLegalMoveByIndex(board, move)
                    break
            except ValueError:
                print("please enter a number or 'go'")

#standalone()

board = 0b101010101101010100101010100000000000000000000000000000000000000000000000000000000000000000000000000000000101010100101010110101010
printBoard(board)
