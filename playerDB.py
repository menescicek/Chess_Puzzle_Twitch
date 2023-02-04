import backendLogic
import re

from helpers.glicko2 import Glicko2
from helpers import helperModule

dbFile = "playerDatabase/ratingDatabase.txt"
dbPlayers = []


def getPlayers():
    db = []
    with open(dbFile, "r+") as file1:
        lines = file1.read()

        regex = r"^\w+\t"
        matches = re.finditer(regex, lines, re.MULTILINE)

        for matchNum, match in enumerate(matches, start=1):
            player = match.group()
            db.append(player.strip())

    print("Databasedeki oyuncular:", db)

    return db


def save():
    print("playerDB.save():", backendLogic.scoreboardDict)
    for key, value in backendLogic.scoreboardDict.items():
        if key in dbPlayers:
            helperModule.replace("playerDatabase/ratingDatabase.txt", r"{}.*".format(key),
                    f"{key}\t{value[2].mu}\t{value[2].sigma}\t{value[2].volatility}")
        else:
            print(f"The key: {key} doesn't exist. record is appended.")
            with open("playerDatabase/ratingDatabase.txt", "a+") as file1:
                file1.write(f"\n{key}\t{value[2].mu}\t{value[2].sigma}\t{value[2].volatility}")


def getRating(playerName):
    with open(dbFile, "r") as file1:
        lines = file1.read()
        regex = fr"{playerName}\t.*$"
        matches = re.finditer(regex, lines, re.MULTILINE)

        for matchNum, match in enumerate(matches, start=1):
            playerRecord = match.group()

    playerName, mu, sigma, volatility = playerRecord.split("\t")

    return getGlickoEnv().create_rating(float(mu), float(sigma), float(volatility))


def getGlickoEnv():
    return Glicko2(tau=0.5)