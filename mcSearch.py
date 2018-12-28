import random
import math
"""
to use, please call:
mcSearch.getAIMove(maxPlayouts, board, getTurn, getLegalMoves, checkForEndByTurn, makeLegalMoveByIndex))

you will need:
a board object (can look like whatever you want)
a getTurn(board) method, returning 1 or 0 depending on whose turn it is
a getLegalMoves(board) method, returning a list of fully legal moves
a checkForEndByTurn(board, moves, player) method,
    which should return 0 for a loss, 0.5 fr a draw, 1 for a win,
    from the point of view of player
a makeLegalMoveByIndex(board, move) method, returning
    a board object with the move made and
    the turn flipped

mcSearch.getAIMove will return the most promising move in the list from getLegalMoves
"""

totalTotal = 0
def selectRandomChild(children):
    return children[random.randint(0, len(children) - 1)]

def selectRandomMove(moves):
    return moves[random.randint(0, len(moves) - 1)]

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


def getRandomGame(board, player, getLegalMoves, checkForEndByTurn, makeLegalMoveByIndex):
    global totalTotal
    totalTotal += 1
    p = player
    while True:
        moves = getLegalMoves(board)
        p = 1 - p
        result = checkForEndByTurn(board, moves, p)
        if result != None:
            if result == 1: #if a win for someone
                if p == player: #if a win for other player
                    result = -result
            return result
        move = selectRandomMove(moves)
        board = makeLegalMoveByIndex(board, move)


class Tree:
    def __init__(self, parent, board, index, player, getLegalMoves):
        self.parent = parent
        self.board = board
        self.score = 0
        self.total = 0
        self.getLegalMoves = getLegalMoves
        self.getMoves(self.getLegalMoves)
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

    def getMoves(self, getLegalMoves):
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

    def simulate(self, getLegalMoves, checkForEndByTurn, makeLegalMoveByIndex):
        result = getRandomGame(self.board, self.player,
        getLegalMoves, checkForEndByTurn, makeLegalMoveByIndex)

        self.total += 1

        if result != -1:
            self.score += result

        if result != 0.5:
            result = -result

        if self.parent != None:
            self.parent.backProp(result, self.index)


    def expand(self, getLegalMoves, checkForEndByTurn, makeLegalMoveByIndex):
        result = checkForEndByTurn(self.board, self.moves, 1 - self.player)
        if result != None:
            return self

        unexploredChildren = [i for i, x in enumerate(self.children) if x == 0]
        if len(unexploredChildren) > 0:
            i = selectRandomChild(unexploredChildren)
            self.getMoves(getLegalMoves)
            newBoard = makeLegalMoveByIndex(self.board, self.moves[i])
            self.children[i] = Tree(self, newBoard, i, 1 - self.player, self.getLegalMoves)
            return self.children[i]

        utcChild = getUCTChildIndex(self.children)
        return self.children[utcChild].expand(getLegalMoves, checkForEndByTurn, makeLegalMoveByIndex)

def mostPlayedKid(children):
    playouts = [0] * len(children)
    for i in range(0, len(children)):
        playouts[i] = children[i].total
    return playouts.index(max(playouts))

def getAIMove(maxPlayouts, board, getTurn, getLegalMoves, checkForEndByTurn, makeLegalMoveByIndex):
    totalTotal = 0
    t = 0
    rootTree = Tree(None, board, -1, getTurn(board), getLegalMoves)
    while t < maxPlayouts:
        t += 1
        selectedTree = rootTree.expand(getLegalMoves, checkForEndByTurn, makeLegalMoveByIndex)
        selectedTree.simulate(getLegalMoves, checkForEndByTurn, makeLegalMoveByIndex)

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
