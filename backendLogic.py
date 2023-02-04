import common
from glicko2 import Glicko2
import re
import helperModule

scoreboardDict, puzzleAnswer, puzzleRating, dbPlayers = dict(), None, None, []


def showPuzzleFromDatabase(pngFilePath, answ, isLastMove=False):
    global puzzleAnswer
    puzzleAnswer = answ

    print("answer:", puzzleAnswer)

    common.placePuzzleImage(pngFilePath, isLastMove)


def updateScoreboardDict(result, ctx):
    print("updateScoreboardDict start:", scoreboardDict)
    if ctx.author.name in dbPlayers:
        userInfo = scoreboardDict.get(f'{ctx.author.name}', [0, ctx.author.is_subscriber,
                                                             getPlayerRatingFromRatingsDatabaseFile(ctx.author.name)])
    else:
        userInfo = scoreboardDict.get(f'{ctx.author.name}', [0, ctx.author.is_subscriber, getDefaultRating()])

    answerCount, isSub, playerRating = userInfo

    if ctx.author.name == "yarabbi":
        isSub = True

    # calculate new rating..
    env = getGlickoEnv()
    newRating = env.rate(playerRating, [(result, env.create_rating(float(puzzleRating), 30))])

    # Update scoreboard..
    scoreboardDict[f'{ctx.author.name}'] = [answerCount + 1, isSub, newRating]
    print("updateScoreboardDict end:", scoreboardDict)

def getPlayersFromRatingsDatabaseFile():
    dbPlayers = []
    with open("ratingDatabase.txt", "r") as file1:
        lines = file1.read()

        regex = r"^\w+\t"
        matches = re.finditer(regex, lines, re.MULTILINE)

        for matchNum, match in enumerate(matches, start=1):
            player = match.group()
            dbPlayers.append(player.strip())

    print("Databasedeki oyuncular:", dbPlayers)

    return dbPlayers


def saveRatingsToDatabaseFile():
    print("saveRatingsToDatabaseFile, scoreboardDict:", scoreboardDict)
    for key, value in scoreboardDict.items():
        if key in dbPlayers:
            helperModule.replace("ratingDatabase.txt", r"{}.*".format(key),
                    f"{key}\t{value[2].mu}\t{value[2].sigma}\t{value[2].volatility}")
        else:
            print("key databasede mevcut değil o yüzden a+ çalıştırıldı.")
            with open("ratingDatabase.txt", "a+") as file1:
                file1.write(f"\n{key}\t{value[2].mu}\t{value[2].sigma}\t{value[2].volatility}")


def getPlayerRatingFromRatingsDatabaseFile(playerName):
    with open("ratingDatabase.txt", "r") as file1:
        lines = file1.read()
        regex = fr"{playerName}\t.*$"
        matches = re.finditer(regex, lines, re.MULTILINE)

        for matchNum, match in enumerate(matches, start=1):
            playerRecord = match.group()

    playerName, mu, sigma, volatility = playerRecord.split("\t")

    return getGlickoEnv().create_rating(float(mu), float(sigma), float(volatility))


def refreshScoreboardItems():
    print("refreshScoreboardItems start:", scoreboardDict)
    common.destroyItems()

    scoreboardSorted = dict(sorted(scoreboardDict.items(), key=lambda x: int(x[1][2].mu), reverse=True))
    for count, (key, value) in enumerate(scoreboardSorted.items()):
        if key == "reverse":
            break

        even = count % 2 == 0
        newItem = common.createNewScoreboardItem((key, value), even)

        common.scoreboardItems.append(newItem)
    print("refreshScoreboardItems end:", scoreboardDict)

def getGlickoEnv():
    return Glicko2(tau=0.5)


def getDefaultRating():
    return getGlickoEnv().create_rating(1500, 200, 0.06)