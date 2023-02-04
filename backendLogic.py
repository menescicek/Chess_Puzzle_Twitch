import common
from helpers.glicko2 import Glicko2
import playerDB

scoreboardDict, puzzleAnswer, puzzleRating = dict(), None, None


def showPuzzleFromDatabase(pngFilePath, answ, isLastMove=False):
    global puzzleAnswer
    puzzleAnswer = answ

    print("answer:", puzzleAnswer)

    common.placePuzzleImage(pngFilePath, isLastMove)


def updateScoreboardDict(result, ctx):
    print("updateScoreboardDict start:", scoreboardDict)
    if ctx.author.name in playerDB.getPlayers():
        userInfo = scoreboardDict.get(f'{ctx.author.name}', [0, ctx.author.is_subscriber,
                                                             playerDB.getRating(ctx.author.name)])
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