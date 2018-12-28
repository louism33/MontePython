import sys
import random
import math

"""
player 1 is x, player 0 is o
0btxxxxxxxxxooooooooo
"""

totalTotal = 0
turnConstant = 0b1000000000000000000
def getTurnBit(board):
    return (board & turnConstant) >> 18

def flipTurn(board):
    return board ^ turnConstant

def selectRandomChild(children):
    return children[random.randint(0, len(children) - 1)]

def selectRandomMove(moves):
    return moves[random.randint(0, len(moves) - 1)]

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
    if getTurnBit(n) == 1:
        sys.stdout.write("It is x's turn")
    else:
        sys.stdout.write("It is o's turn")
    sys.stdout.write("\n")
    sys.stdout.write("\n")

def getRandomChild(children):
    return random.randint(0, len(children) - 1)

explorationParameter =  1.414 #root two

def getUCTChildIndex(children):
    utcScores = [0] * len(children)
    for i in range(0, len(children)):
        child = children[i]
        rank = ((child.score / child.total)
         + explorationParameter *
         (math.sqrt((math.log(totalTotal)) / child.total)))
        utcScores[i] = rank
    return utcScores.index(max(utcScores))


def getRandomGame(board, player):
    global totalTotal
    totalTotal += 1
    p = player
    while True:
        moves = getLegalMoves(board)
        p = 1 - p
        result = checkForEndByTurn(board, moves, p)
        if result != None:
            #print("random board: ")
            #printBoard(board)
            if result == 1: #if a win for someone
                if p == player: #if a win for other player
                    result = -result
            return result
        move = selectRandomMove(moves)
        board = makeLegalMoveSafeIndex(board, move)


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

def makeLegalMoveSafeIndex(board, n):
    moves = getLegalMoves(board)
    if n in moves:
        n = 2 ** n
        if getTurnBit(board) == 1:
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



class Tree:
    def __init__(self, parent, board, index, player):
        self.parent = parent
        self.board = board
        self.score = 0
        self.total = 0
        self.getMoves()
        self.index = index
        self.children = [0] * len(self.moves)
        self.player = player

    def __str__(self):
        self.getMoves()
        return (str(self.score) + "/" + str(self.total)
        + "\ntotal is: " + str(self.total) + ", score: "
        + str(self.score) + ", moves: " + str(self.moves)
        + "\nplayer is: " + str(self.player)
        )

    def getMoves(self):
        self.moves = getLegalMoves(self.board)
        return self.moves

    def backProp(self, result, i):
        self.total += 1
        if result != -1:
            self.score += result

        if result != 0.5:
            result = -result

        if self.parent != None:
            self.parent.backProp(result, self.index)

    def simulate(self):
        result = getRandomGame(self.board, self.player)
        self.total += 1

        if result != -1:
            self.score += result

        if result != 0.5:
            result = -result

        if self.parent != None:
            self.parent.backProp(result, self.index)


    def expand(self):
        result = checkForEndByTurn(self.board, self.moves, 1 - self.player)
        if result != None:
            return self

        unexploredChildren = [i for i, x in enumerate(self.children) if x == 0]
        if len(unexploredChildren) > 0:
            i = selectRandomChild(unexploredChildren)
            self.getMoves()
            newBoard = makeLegalMoveSafeIndex(self.board, self.moves[i])
            self.children[i] = Tree(self, newBoard, i, 1 - self.player)
            return self.children[i]

        utcChild = getUCTChildIndex(self.children)
        return self.children[utcChild].expand()

def mostPlayedKid(children):
    playouts = [0] * len(children)
    for i in range(0, len(children)):
        playouts[i] = children[i].total
    return playouts.index(max(playouts))

def getAIMove(board):
    totalTotal = 0
    t = 0
    rootTree = Tree(None, board, -1, getTurnBit(board))
    while t < 5000:
        t += 1
        selectedTree = rootTree.expand()
        selectedTree.simulate()

    bestMoveIndex = mostPlayedKid(rootTree.children)
    #childrenBreakdown(rootTree)
    return rootTree.moves[bestMoveIndex]

def childrenBreakdown(tree):
    print()
    print("----- Parent node-----")
    print()
    print(tree)
    printBoard(tree.board)
    print()
    print("\n-----Children breakdown-----\n")
    for t in tree.children:
        if t != 0:
            printBoard(t.board)
            print(t)


def standalone():
    board = 0b1000000000000000000
    while True:
        printBoard(board)
        moves = getLegalMoves(board)
        player = getTurnBit(board)
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
                board = makeLegalMoveSafeIndex(board, getAIMove(board))
                break
            try:
                move = int(m)
                if move in moves:
                    board = makeLegalMoveSafeIndex(board, move)
                    break
            except ValueError:
                print("please enter a number or 'go'")

standalone()
