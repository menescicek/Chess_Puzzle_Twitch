import re
from game import *
import os, sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def convertSquareToInt(sq):
    col = int(sq[1])
    row = ord(sq[0]) - ord('a')

    return row + (col-1)* 8

def extractPGN(fullGameInfo):
    print(fullGameInfo)
    games = []

    pgns = []
    whiteInfo = []
    blackInfo = []
    whiteEloInfo = []
    blackEloInfo = []
    variants = []

    regex = r"\[Variant \"\w+\s*\w+\"\]"
    matches = re.finditer(regex, fullGameInfo, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        variant = match.group()
        variants.append(variant[10:-2])

    regex = r"(?<=1).*?(?=(1-0|0-1|1/2-1/2))"
    matches = re.finditer(regex, fullGameInfo, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        pgns.append("1" + match.group())

    regex = r"\[White \"\w+\"\]"
    matches = re.finditer(regex, fullGameInfo, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        whiteInfo.append(match.group())

    regex = r"\[Black \"\w+\"\]"
    matches = re.finditer(regex, fullGameInfo, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        blackInfo.append(match.group())


    regex = r"\[WhiteElo \"\w+\"\]"
    matches = re.finditer(regex, fullGameInfo, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        whiteEloInfo.append(match.group())


    regex = r"\[BlackElo \"\w+\"\]"
    matches = re.finditer(regex, fullGameInfo, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        blackEloInfo.append(match.group())


    for i in range(len(pgns)):
        if variants[i] == 'Standard':
            game = Game()
            game.set_pgn(pgns[i])
            game.set_white(whiteInfo[i])
            game.set_black(blackInfo[i])
            game.set_whiteElo(whiteEloInfo[i])
            game.set_blackElo(blackEloInfo[i])
            games.append(game)

    return games