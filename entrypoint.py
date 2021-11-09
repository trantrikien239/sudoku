from src.game_play.puzzle_reader import read_jl_file
from src.solvers.backtrack import BacktrackSolver
from src.solvers.human_tactic import HumanTactic

i = 0
for board in read_jl_file('./puzzles/websudoku.jl'):
    print(board)
    bts = HumanTactic(board)
    # bts.solve()
    bts.solve_human()
    i += 1
    if i >= 5:
        break