from stockfish import Stockfish
from copy import copy


stockfish = Stockfish(path= ".\MOTOR\stockfish_15_x64.exe",
                      depth=5,
                      parameters={"Threads": 2, "Minimum Thinking Time": 1})

def generatePuzzle(board, puzzles, game, move):
    stockfish.set_fen_position(board.fen())
    topmoves = stockfish.get_top_moves()
    if len(topmoves) >= 2:
        bestMove = topmoves[0]
        secondBestMove = topmoves[1]
        ans = ""
        if bestMove["Mate"] == None and secondBestMove["Mate"] == None:
            cp = bestMove["Centipawn"]
            if abs(cp) > 300 and -70 < secondBestMove["Centipawn"] and secondBestMove["Centipawn"] < 70:
                ans = bestMove["Move"]

        if ans != "":
            temp = copy(board)
            puzzles.append((ans, temp, game, move))
