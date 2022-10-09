import numpy as np
import sys

from src.solvers.backtrack import BacktrackSolver
from src.solvers.human_tactic import HumanTactic



if __name__ == "__main__":
    if sys.argv[1] in ("Backtrack", "BacktracSolver"):
        SolverClass = BacktrackSolver
    elif sys.argv[1] in ("Human", "HumanTactic"):
        SolverClass = HumanTactic
    else:
        raise ValueError("Solver not exist, try `Backtrack` or `Human`")
    
    # Easy
    # board = np.array([
    #     [6,0,9,5,0,7,8,0,0],
    #     [0,7,4,2,0,0,0,0,0],
    #     [2,0,0,0,8,0,0,0,7],
    #     [5,0,8,0,9,0,2,0,4],
    #     [0,9,0,0,0,0,0,5,0],
    #     [4,0,1,0,6,0,3,0,8],
    #     [7,0,0,0,1,0,0,0,9],
    #     [0,0,0,0,0,6,5,4,0],
    #     [0,0,6,9,0,4,7,0,3]
    # ])
    # # Expert
    # board = np.array([
    #     [0,0,7,0,5,0,0,0,0],
    #     [6,0,4,0,0,3,0,0,0],
    #     [9,5,0,0,0,0,7,0,0],
    #     [2,0,0,5,0,0,0,6,0],
    #     [7,0,0,0,9,0,0,0,1],
    #     [0,1,0,0,0,6,0,0,8],
    #     [0,0,9,0,0,0,0,7,5],
    #     [0,0,0,1,0,0,6,0,3],
    #     [0,0,0,0,2,0,1,0,0],
    # ])
    # board = np.array([
    #     [0,0,0,0,0,0,0,6,0],
    #     [2,0,0,5,0,0,0,1,9],
    #     [0,8,0,3,0,9,0,0,4],
    #     [0,0,0,1,7,0,0,9,0],
    #     [0,0,2,0,0,0,8,0,0],
    #     [0,5,0,0,3,2,0,0,0],
    #     [7,0,0,4,0,1,0,3,0],
    #     [6,1,0,0,0,7,0,0,5],
    #     [0,4,0,0,0,0,0,0,0],
    # ])
    board = np.array([
        [0,8,0,0,0,0,2,0,0],
        [0,1,0,0,0,9,3,0,6],
        [0,5,0,6,0,0,7,0,0],
        [0,0,7,8,0,6,0,0,0],
        [0,0,0,5,0,2,0,0,0],
        [0,0,0,3,0,4,1,0,0],
        [0,0,3,0,0,8,0,4,0],
        [4,0,5,2,0,0,0,6,0],
        [0,0,8,0,0,0,0,2,0],
    ])
    
    solver = SolverClass(board)
    solver.solve()