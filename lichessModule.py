import lichess.api
from lichess.format import SINGLE_PGN

def getInfo(username):
    return lichess.api.user_games(username, max = 5, format = SINGLE_PGN)
