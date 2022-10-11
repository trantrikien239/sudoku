import json
import time
import numpy as np
import pandas as pd

from .backtrack import BacktrackSolver
from .human_tactic import HumanTactic

def read_game(game_path):
    with open(game_path) as f:
        for line in f:
            game = json.loads(line)
            result = np.reshape([int(e) for e in game['result']], (9,9))
            mask = np.reshape([int(e) for e in game['display']], (9,9))
            game["board"] = result * mask
            game["result"] = result
            yield(game)

def bulk_solve(game_path, solver_class):
    games = read_game(game_path)
    meas = pd.DataFrame({
        'game_level':[],
        'game_id':[],
        'solve_correct': [],
        'solve_time': []
    })
    for game in games:
        board = game["board"]
        result = game["result"]
        s_ = time.time()
        solver = solver_class(board)
        output = solver.solve()
        f_ = time.time()
        df_out = pd.DataFrame([[
            int(game['level']), 
            int(game['id']),
            (result == output).all(),
            f_ - s_
            ]], columns=["game_level", "game_id", "solve_correct", "solve_time"])
        meas = pd.concat([meas, df_out], ignore_index=True)
    return meas
            

    

if __name__ == '__main__':
    bulk_solve("./puzzles/games_lite.jl", HumanTactic)