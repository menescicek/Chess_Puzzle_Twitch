import pandas as pd
import random
import chess
import re
import cairoModule as cm
import time
import helperModule

index = 0
board = None
moves = None

svgFile = 'pos.svg'
def getPuzzles(startReadingFunction, stopReadingFunction, showPuzzleFromDatabaseFunction):
    global index, board, moves


    startReadingFunction()


    randomNumber = random.randint(1, 3000000)

    colnames = ['PuzzleId','FEN','Moves','Rating','RatingDeviation','Popularity','NbPlays','Themes','GameUrl','OpeningFamily','OpeningVariation']
    df = pd.read_csv('DATABASE/lichess_db_puzzle.csv', on_bad_lines='skip', names= colnames, usecols=['FEN','Moves', 'Rating'])
    print(randomNumber)
    df = df.iloc[[randomNumber], [0, 1, 2]]
    fen = df.iloc[0][0]
    movesString = df.iloc[0][1]
    rating = df.iloc[0][2]

    print("FEN:", fen)
    print("Moves:", movesString)
    print("Rating:", rating)


    regex = r"\w+"
    matches = re.finditer(regex, movesString)
    moves = []
    for matchNum, match in enumerate(matches, start=1):
        moves.append(match.group())

    board = chess.Board()
    board.set_fen(fen)

    firstPosition(showPuzzleFromDatabaseFunction)

    stopReadingFunction()

    time.sleep(1)
    index = 0
    computerMove(index, showPuzzleFromDatabaseFunction)

def firstPosition(func):
    with open(svgFile, 'w') as f:
        f.write(chess.svg.board(board))
    puzzlePngFilePath = cm.convert2Png(svgFile)
    ans = ""
    func(puzzlePngFilePath, ans)

def computerMove(index, func):
    moveToPush = moves[index]
    print("Computer Move: ", moveToPush)

    firstSqr = moveToPush[:2]
    secondSqr = moveToPush[2:]
    board.push_san(moveToPush)

    with open(svgFile, 'w') as f:
        f.write(chess.svg.board(board, arrows=[
            chess.svg.Arrow(helperModule.convertSquareToInt(firstSqr), helperModule.convertSquareToInt(secondSqr))]))
    puzzlePngFilePath = cm.convert2Png(svgFile)


    ans = moves[index + 1]
    func(puzzlePngFilePath, ans)

def checkMoveValid(index):
    if index > len(moves) - 1:
        return False
    else:
        return True

def playerMove(index, func):
    moveToPush = moves[index]
    print("Player Move: ", moveToPush)

    board.push_san(moveToPush)

    firstPosition(func)

def onCorrectMoveFound(showPuzzleFromDatabaseFunction):
    global index, moves
    index += 1
    if checkMoveValid(index):
        playerMove(index, showPuzzleFromDatabaseFunction)
    else:
        print("Puzzle Solved!")
        return
    index += 1
    if checkMoveValid(index):
        computerMove(index, showPuzzleFromDatabaseFunction)
    else:
        print("Puzzle Solved!")
        return