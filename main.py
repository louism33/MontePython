# a basic noughts and crosses game in python
import sys
import util.util
import random

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
            #sys.stdout.write(str(t-1)+" | ")
            sys.stdout.write(". | ")
        mask = mask * 2
        if ((t % 3 == 0) & (t < 8)):
            sys.stdout.write("\n | ")
    sys.stdout.write("\n")
    sys.stdout.write("\n")
    if getTurnBit(n):
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

    if len(getLegalMoves(board)) == 0:
        return 0

    for i in range(-1, 2, 2):
        if i == 1:
            board = board >> 9
        if rowOne & board == rowOne:
            return i
        if rowTwo & board == rowTwo:
            return i
        if rowThree & board == rowThree:
            return i

        if colOne & board == colOne:
            return i
        if colTwo & board == colTwo:
            return i
        if colThree & board == colThree:
            return i

        if diag & board == diag:
            return i
        if antiDiag & board == antiDiag:
            return i
    return None

def standalone():
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
                    printBoard(board)
                    print("win for o")
                    return 1
                if result == -1:
                    printBoard(board)
                    print("win for x")
                    return -1
                break

def selectRandomMove(moves):
    return moves[random.randint(0, len(moves) - 1)]

def getRandomGame(board):
    while True:
        result = checkForEnd(board)
        if result != None:
            return result

        moves = getLegalMoves(board)
        if len(moves) == 0:
            return 0
        move = selectRandomMove(moves)
        board = makeLegalMoveSafeIndex(board, move)
        result = checkForEnd(board)
        if result == 1:
            return 1
        if result == -1:
            return -1

def selectRandomRootIndex(moves):
    return random.randint(0, len(moves) - 1)

class Tree:
    def __init__(self, parent, board, index):
        self.parent = parent
        self.board = board
        self.score = 0
        self.total = 0
        self.getMoves()
        self.index = index
        self.children = [0] * len(self.moves)
        self.childrenScores = [0] * len(self.moves)

    def __str__(self):
        self.getMoves()
        return ("total is: " + str(self.total) + ", score: "
        + str(self.score) + ", moves: " + str(self.moves)
        #+ "\nchildren: " + str(self.children)
        + "\nchildren scores: " + str(self.childrenScores))

    def getMoves(self):
        self.moves = getLegalMoves(self.board)
        return self.moves

    def backProp(self, result, i):
        self.total += 1
        self.score += result
        self.childrenScores[i] += result

        if self.parent != None:
            #self.parent.childrenScores[i] += a
            self.parent.backProp(result, self.index)

    def simulate(self):
        a = getRandomGame(self.board)
        self.total += 1
        self.score += a
        if self.parent != None:
            self.parent.backProp(a, self.index)


    def expand(self):
        result = checkForEnd(self.board)
        if result != None:
            """
            self.total += 1
            self.score += result
            if self.parent != None:
                self.parent.backProp(result, self.index)
            """
            return self

        else:
            self.getMoves()
            i = selectRandomRootIndex(self.moves)
            move = self.moves[i]

            if self.children[i] == 0:
                newBoard = makeLegalMoveSafeIndex(self.board, i)
                self.children[i] = Tree(self, newBoard, i)
                return self.children[i]
            else:
                return self.children[i].expand()


"""
selection expansion simulation backprop
"""

def getAIMove():
    global masterBoard
    t = 0

    rootTree = Tree(None, masterBoard, -1)
    #print("Root tree:")
    #printBoard(rootTree.board)

    while t < 10000:
        t += 1
        selectedTree = rootTree.expand()
        selectedTree.simulate()

    if getTurnBit(rootTree.board):
        bestMoveIndex = rootTree.childrenScores.index(max(rootTree.childrenScores))
    else:
        bestMoveIndex = rootTree.childrenScores.index(min(rootTree.childrenScores))

    return rootTree.moves[bestMoveIndex]


def childrenBreakdown(tree):
    print()
    print()
    print("\n-----Children breakdown-----\n")
    for t in tree.children:
        if t != 0:
            printBoard(t.board)
            print(t)

masterBoard = 0b1000000000000000000
#board = 0b11000000000000110

print(getAIMove())
