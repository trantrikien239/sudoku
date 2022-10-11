import numpy as np
import sys

from src.solvers.backtrack import BacktrackSolver
from src.solvers.human_tactic import HumanTactic
from src.solvers.solve import bulk_solve



if __name__ == "__main__":
    df1 = bulk_solve("./puzzles/games.jl", HumanTactic)
    df1.to_parquet("./human.parquet")
    df2 = bulk_solve("./puzzles/games.jl", BacktrackSolver)
    df2.to_parquet("./backtrack.parquet")
    