def getPuzzles():
    pass


def onCorrectMoveFound():
    pass


def startReading():
    pass


def stopReading():
    pass


def showPuzzleFromDatabase():
    pass


def showPuzzleInfo():
    pass


def onExceptionOccured():
    pass


def startGui():
    pass


def fillAndDisplayPatronsFrame():
    pass


def placePuzzleImage():
    pass


def destroyItems():
    pass


def createNewScoreboardItem():
    pass


def login():
    pass


streamerName = ""
scoreboardItems = []
readyDestroyLoginWindow = False
readyOpenMainWindow = False
autherror = False


from createPuzzle import getPuzzles, onCorrectMoveFound
from gui import startReading, stopReading, showPuzzleInfo, onExceptionOccured, \
    startGui, refreshPatrons, placePuzzleImage, destroyItems, createNewScoreboardItem, scoreboardItems, login