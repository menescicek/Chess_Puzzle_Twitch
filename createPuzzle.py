import numpy
import pandas as pd
import random
import chess
import chess.svg
import re
import time
from helpers import helperModule, cairoModule as cm

import common
import backendLogic as backend

index = 0
board = None
moves = None

svgFile = 'pos.svg'
WHITE = ""
waitingTime = 1


def convert(val):
    if val == numpy.NaN:
        return 0
    return val


def getPuzzles(mode):
    global index, board, moves, WHITE

    common.startReading()
    try:
        if mode == 1:
            n = 962408
            rand = random.randint(1, n)
            df = pd.read_csv('puzzleDatabase/15002000.csv', skiprows= rand, nrows= 1, engine='c', header= None, dtype={
                         "0": "str",
                         "1": "str",
                         "2": "str",
                         "3": "int",
                         "4": "int",
                         "5": "int",
                         "6": "int",
                         "7": "str",
                         "8": "str",
                         "9": "int"
                     }, converters= {"9": convert})
            print("15002000:", df[df.columns[0]].count())
        elif mode == 2:
            n = 522107
            rand = random.randint(1, n)
            df = pd.read_csv('puzzleDatabase/20002500.csv', skiprows=rand, nrows=1, engine='c', header=None, dtype={
                "0": "str",
                "1": "str",
                "2": "str",
                "3": "int",
                "4": "int",
                "5": "int",
                "6": "int",
                "7": "str",
                "8": "str",
                "9": "int"
            }, converters={"9": convert})
            print("20002500:", df[df.columns[0]].count())

        elif mode == 3:
            n = 107888
            rand = random.randint(1, n)
            df = pd.read_csv('puzzleDatabase/25003000.csv', skiprows=rand, nrows=1, engine='c', header=None, dtype={
                "0": "str",
                "1": "str",
                "2": "str",
                "3": "int",
                "4": "int",
                "5": "int",
                "6": "int",
                "7": "str",
                "8": "str",
                "9": "int"
            }, converters={"9": convert})
            print("25003000:", df[df.columns[0]].count())

        print(df)
        # print(df.columns.values)
        print(df.iloc[0])
        fen = df.iloc[0][2]
        movesString = df.iloc[0][3]
        rating = df.iloc[0][4]
        popularity = df.iloc[0][5]
        themes = df.iloc[0][6]
        gameurl = df.iloc[0][7]

        data = [str(rating), str(popularity), str(themes), str(gameurl)]

        print("FEN:", fen)
        print("Moves:", movesString)
        print("Rating:", rating)
        print("Popularity:", popularity)
        print("Themes:", themes)
        print("Gameurl:", gameurl)

        regex = r"\w+"
        matches = re.finditer(regex, movesString)
        moves = []
        for matchNum, match in enumerate(matches, start=1):
            moves.append(match.group())

        board = chess.Board()
        board.set_fen(fen)
        WHITE = board.turn

    except Exception as e:
        print("Bir hata oluştu:...::", e)

        common.onExceptionOccured()

        common.stopReading()
    else:

        common.showPuzzleInfo(data)
        print("Turn: ", board.turn)

        firstPosition()

        common.stopReading()
        time.sleep(waitingTime)
        index = 0

        computerMove(index)


def firstPosition(isLastMove = False):
    with open(svgFile, 'w') as f:
        if WHITE:
            f.write(chess.svg.board(board, orientation= chess.BLACK))
        else:
            f.write(chess.svg.board(board, orientation=chess.WHITE))

    puzzlePngFilePath = cm.convert2Png(svgFile)
    ans = ""
    backend.showPuzzleFromDatabase(puzzlePngFilePath, ans, isLastMove)


def computerMove(index):
    moveToPush = moves[index]
    print("Computer Move: ", moveToPush)

    firstSqr = moveToPush[:2]
    secondSqr = moveToPush[2:]
    board.push_san(moveToPush)

    with open(svgFile, 'w') as f:
        if WHITE:
            f.write(chess.svg.board(board, orientation=chess.BLACK, arrows=[
                chess.svg.Arrow(helperModule.convertSquareToInt(firstSqr), helperModule.convertSquareToInt(secondSqr))]))
        else:
            f.write(chess.svg.board(board, orientation=chess.WHITE, arrows=[
                chess.svg.Arrow(helperModule.convertSquareToInt(firstSqr),
                                helperModule.convertSquareToInt(secondSqr))]))
    puzzlePngFilePath = cm.convert2Png(svgFile)


    ans = moves[index + 1]
    backend.showPuzzleFromDatabase(puzzlePngFilePath, ans)


def checkMoveValid(index):
    if index > len(moves) - 1:
        return False
    else:
        return True


def playerMove(index, isLastMove = False):
    moveToPush = moves[index]
    print("Player Move: ", moveToPush)

    board.push_san(moveToPush)

    firstPosition(isLastMove)


def onCorrectMoveFound():
    global index, moves
    index += 1
    if checkMoveValid(index):
        isLastMove = not checkMoveValid(index + 1)
        playerMove(index, isLastMove)
    else:
        print("Puzzle Solved! After Computer")

        return
    index += 1
    if checkMoveValid(index):
        computerMove(index)
    else:
        print("Puzzle Solved! After Player")
        return