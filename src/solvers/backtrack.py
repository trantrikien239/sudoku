import numpy as np 
import itertools
from copy import deepcopy
import sys
from os.path import abspath, join as join_path
sys.path.insert(0,abspath(join_path(abspath(__file__),'../..')))
# print(sys.path)
from game_play.rules import Game


class BacktrackSolver(Game):
    def __init__(self, game_board):
        super(BacktrackSolver,self).__init__()
        self.original_puzzle = deepcopy(game_board)
        self.board = game_board

    INDEX = {}
    for cnt, p in zip(
        range(9 ** 9), 
        itertools.product(range(9), range(9))
        ):
        INDEX[cnt] = (p[0], p[1])

    @staticmethod
    def check_1to9_not_duplicate(ndarray):
        flt = [x for x in ndarray.flatten() if x != 0]
        return len(flt) == len(set(flt))
    
    # @staticmethod
    # def get_

    def check_cell(self,i,j):
        not_conflict = True
        not_conflict = not_conflict and self.board[i,j] > 0
        not_conflict = not_conflict and self.board[i,j] <= 9
        not_conflict = not_conflict and self.check_1to9_not_duplicate(self.board[i,:])
        not_conflict = not_conflict and self.check_1to9_not_duplicate(self.board[:,j])
        region = self.get_board_regions()[i//self.AREA_SIZE, j//self.AREA_SIZE]
        not_conflict = not_conflict and self.check_1to9_not_duplicate(region)
        return not_conflict
        
    def cell_consistent_try(self,cnt):
        # import pdb; pdb.set_trace()
        self.board[self.INDEX[cnt]] += 1
        while not self.check_cell(*self.INDEX[cnt]):
            if self.board[self.INDEX[cnt]] < 9:
                self.board[self.INDEX[cnt]] += 1
                # print(cnt)
            else:
                self.board[self.INDEX[cnt]] = 0
                return False
        return True

    def cell_not_original(self,cnt):
        if self.original_puzzle[self.INDEX[cnt]] == 0:
            return True
        else:
            return False


    def solve(self):
        cnt = 0
        direction = 1

        # print(self.INDEX)

        while cnt < 81:
            if self.cell_not_original(cnt):
                if self.cell_consistent_try(cnt):
                    cnt += 1
                    direction = 1
                    print(cnt, direction)
                else:
                    cnt -= 1
                    direction = -1
                    print('back_tracking: ', cnt, direction)
            else:
                cnt += 1 * direction
            
        # import pdb; pdb.set_trace()
        if not self.check_solution():
            print('The puzzle is infeasible')
            print('The solution is: \n', self.board)
        else:
            print('The solution is: \n', self.board)


if __name__ == '__main__':
    board = np.array([
        [6,0,9,5,0,7,8,0,0],
        [0,7,4,2,0,0,0,0,0],
        [2,0,0,0,8,0,0,0,7],
        [5,0,8,0,9,0,2,0,4],
        [0,9,0,0,0,0,0,5,0],
        [4,0,1,0,6,0,3,0,8],
        [7,0,0,0,1,0,0,0,9],
        [0,0,0,0,0,6,5,4,0],
        [0,0,6,9,0,4,7,0,3]
    ])
    solver = BacktrackSolver(board)
    solver.solve()