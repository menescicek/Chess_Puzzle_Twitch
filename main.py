import io

import chess.svg

import lichessModule as lm
from stckfshModule import *
import helperModule
import cairoModule as awm




from chess.pgn import *

def main(username, func1, func2, func3, func4, func5, func6):
    func6("")
    if username == "":
        func2()
        return

    try:
        fullInfo = lm.getInfo(username)
    except Exception as e:
        func3()
        print(e)
    else:
        games = helperModule.extractPGN(fullInfo)
        func4()
        gameNo = 0

        puzzleInfo = []
        for game in games:

            board = chess.pgn.read_game(io.StringIO(game.pgn)).board()
            puzzles = []
            moveNo = 1
            for move in chess.pgn.read_game(io.StringIO(game.pgn)).mainline_moves():
                print()
                func6("Looking at :"+  str(moveNo) +  " " +  str(move))
                board.push(move)

                generatePuzzle(board, puzzles, game, move)
                moveNo += 1

            k = 0
            # puzzle ---> ans board game
            for puzzle in puzzles:

                # create .svg file
                svgFile = 'pos{}{}.svg'.format(gameNo, k)
                with open(svgFile, 'w') as f:
                    move = str(puzzle[3])
                    firstSqr = move[:2]
                    secondSqr = move[2:]
                    print(helperModule.convertSquareToInt(firstSqr))

                    # arrows =
                    f.write(chess.svg.board(puzzle[1], arrows= [chess.svg.Arrow(helperModule.convertSquareToInt(firstSqr), helperModule.convertSquareToInt(secondSqr))]))

                puzzleInfo.append((awm.convert2Png(svgFile), puzzle[0], puzzle[2]))


                k += 1

            gameNo += 1

        func1(puzzleInfo)
        func5()

