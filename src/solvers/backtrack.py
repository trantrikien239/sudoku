import numpy as np 
import itertools
from copy import deepcopy
import sys
from os.path import abspath, join as join_path
sys.path.insert(0,abspath(join_path(abspath(__file__),'../..')))
# print(sys.path)
from game_play.rules import Game
import time
import pdb

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed

class BacktrackSolver(Game):
    def __init__(self, game_board):
        super(BacktrackSolver,self).__init__()
        self.original_puzzle = deepcopy(game_board)
        self.board_for_sure = deepcopy(game_board)
        self.board = game_board
        self.INDEX = {}
        self.INDEX_REVERSE = {}
        for cnt, p in zip(
            range(self.GRID_SIZE * self.GRID_SIZE), 
            itertools.product(range(self.GRID_SIZE), range(self.GRID_SIZE))
            ):
            self.INDEX[cnt] = (p[0], p[1])
            self.INDEX_REVERSE[(p[0], p[1])] = cnt
        
        
        # import pdb; pdb.set_trace()

    @staticmethod
    def check_1to9_not_duplicate(ndarray):
        flt = [x for x in ndarray.flatten() if x != 0]
        return len(flt) == len(set(flt))
    

    def check_cell(self,i,j):
        not_conflict = True
        not_conflict = not_conflict and self.board[i,j] > 0
        not_conflict = not_conflict and self.board[i,j] <= self.GRID_SIZE
        not_conflict = not_conflict and self.check_1to9_not_duplicate(self.board[i,:])
        not_conflict = not_conflict and self.check_1to9_not_duplicate(self.board[:,j])
        region = self.get_board_regions()[i//self.AREA_SIZE, j//self.AREA_SIZE]
        not_conflict = not_conflict and self.check_1to9_not_duplicate(region)
        return not_conflict
        
    def cell_consistent_try(self,coor):
        self.board[coor] += 1
        while not self.check_cell(*coor):
            if self.board[coor] < self.GRID_SIZE:
                self.board[coor] += 1
                # print(coor)
            else:
                self.board[coor] = 0
                return False
        return True

    # def cell_not_original(self,coor):
    #     if self.original_puzzle[coor] == 0:
    #         return True
    #     else:
    #         return False

    def cell_not_for_sure(self,coor):
        if self.board_for_sure[coor] == 0:
            return True
        else:
            return False

    @timeit
    def solve(self):
        cnt = 0
        direction = 1
        self.board = deepcopy(self.board_for_sure)
        # print(self.INDEX)
        cnt_iteration = 0
        cnt_forward = 0
        cnt_backtrack = 0
        while cnt < 81:
            cnt_iteration += 1
            if self.cell_not_for_sure(self.INDEX[cnt]):
                if self.cell_consistent_try(self.INDEX[cnt]):
                    cnt += 1
                    direction = 1
                    cnt_forward += 1
                else:
                    cnt -= 1
                    direction = -1
                    cnt_backtrack += 1
                    # if cnt == 0 and direction == -1:
                    #     print('The puzzle is infeasible')
                    #     print('Last board: \n', self.board)
                    #     sys.exit()
            else:
                cnt += 1 * direction
            
        # import pdb; pdb.set_trace()
        print(f'Number of iteration: {cnt_iteration}')
        print(f'Number of forward: {cnt_forward}')
        print(f'Number of backtrack: {cnt_backtrack}')
        if not self.check_solution():
            print('The puzzle is infeasible')
            print('Last board: \n', self.board)
        else:
            print('The solution is: \n', self.board)

class BacktrackProba(BacktrackSolver):
    def __init__(self, game_board):
        super(BacktrackProba,self).__init__(game_board)

    def get_proba_sequence(self):
        # for cnt, p in zip(
        #     range(self.GRID_SIZE ** self.GRID_SIZE), 
        #     itertools.product(range(self.GRID_SIZE), range(self.GRID_SIZE))
        #     ):
        #     self.INDEX[cnt] = (p[0], p[1])
        count_possibilities = []
        i_j = []
        # position = list(range(self.GRID_SIZE ** self.GRID_SIZE))
        for i,j in itertools.product(range(self.GRID_SIZE), range(self.GRID_SIZE)):
            i_j.append((i,j))
            if self.original_puzzle[i,j] == 0:
                row = self.board[i,:]
                column = self.board[:,j]
                region = self.get_board_regions()[i//self.AREA_SIZE, j//self.AREA_SIZE]
                count_possibilities.append(self.GRID_SIZE - len([x for x in set(np.concatenate((
                    row.flatten(), 
                    column.flatten(), 
                    region.flatten())
                    ).flatten()
                ) if x != 0]))
            else:
                count_possibilities.append(10)

        print('Getting possibilities')
        
        for _ in range(self.GRID_SIZE * self.GRID_SIZE - 2):
            for i in range(self.GRID_SIZE * self.GRID_SIZE - 2):
                if count_possibilities[i] > count_possibilities[i+1]:
                    count_possibilities[i], count_possibilities[i+1] = count_possibilities[i+1], count_possibilities[i]
                    i_j[i], i_j[i+1] = i_j[i+1], i_j[i] 
                    # position[i], position[i+1] = position[i+1], position[i]

        index_dict = {}
        possibilities_map = np.array(self.DUMMY_BACKGROUND)

        for i in range(len(i_j)):
            index_dict[i] = i_j[i]
            possibilities_map[i_j[i]] = count_possibilities[i]
        print(f'Done getting possibilities: \n {possibilities_map}')
        print(index_dict)
        
        self.INDEX = index_dict
        return index_dict

    



if __name__ == '__main__':
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
    board = np.array([
        [0,0,0,0,0,0,0,6,0],
        [2,0,0,5,0,0,0,1,9],
        [0,8,0,3,0,9,0,0,4],
        [0,0,0,1,7,0,0,9,0],
        [0,0,2,0,0,0,8,0,0],
        [0,5,0,0,3,2,0,0,0],
        [7,0,0,4,0,1,0,3,0],
        [6,1,0,0,0,7,0,0,5],
        [0,4,0,0,0,0,0,0,0],
    ])
    # board = np.array([
    #     [0,8,0,0,0,0,2,0,0],
    #     [0,1,0,0,0,9,3,0,6],
    #     [0,5,0,6,0,0,7,0,0],
    #     [0,0,7,8,0,6,0,0,0],
    #     [0,0,0,5,0,2,0,0,0],
    #     [0,0,0,3,0,4,1,0,0],
    #     [0,0,3,0,0,8,0,4,0],
    #     [4,0,5,2,0,0,0,6,0],
    #     [0,0,8,0,0,0,0,2,0],
    # ])
    # solver = BacktrackSolver(board)
    solver = HumanTactic(board)
    # solver.get_proba_sequence()
    solver.solve_human()