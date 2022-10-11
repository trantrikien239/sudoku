import numpy as np
import itertools

from .backtrack import BacktrackSolver, timeit

class HumanTactic(BacktrackSolver):
    def __init__(self, game_board):
        super(HumanTactic,self).__init__(game_board)
        self.possibilities = {}

    def _get_set_coor(self, coor):
        row_coor = [(coor[0],i) for i in range(self.GRID_SIZE)]
        col_coor = [(j, coor[1]) for j in range(self.GRID_SIZE)]
        # region_ind = []
        reg_min_row = (coor[0] // 3) * 3
        reg_min_col = (coor[1] // 3) * 3
        region_coor = list(itertools.product(
            range(reg_min_row, reg_min_row + 3),
            range(reg_min_col, reg_min_col + 3)
            ))
        return row_coor, col_coor, region_coor
        
    def check_possibiities_all_direction(self, print_board=False):
        for ind, coor in self.INDEX.items():
            if self.board_for_sure[coor] != 0:
                # If the value of the index is true for sure, let it be
                self.possibilities[ind] = [self.board_for_sure[coor]]
            else:
                # If the value is not for sure, check all the value in the same
                # row, column and region with it
                row = self.board_for_sure[coor[0],:]
                column = self.board_for_sure[:,coor[1]]
                region = self.get_board_regions()[coor[0]//self.AREA_SIZE, coor[1]//self.AREA_SIZE]

                self.possibilities[ind] = [x for x in range(1,10) \
                    if x not in set(np.concatenate((
                        row.flatten(), 
                        column.flatten(), 
                        region.flatten())
                        ).flatten()
                    )
                ]

    def check_num_poss(self, val, set_coor, ind):
        set_poss = []
        for coor_x in set_coor:
            set_poss += self.possibilities[self.INDEX_REVERSE[coor_x]]
        num_poss = [x for x in set_poss if x == val]
        return len(num_poss)

    def update_board_for_sure(self):
        for ind, coor in self.INDEX.items():
            if self.board_for_sure[coor] != 0:
                # If the value of the index is true for sure, let it be
                pass
            else:
                if self.possibilities[ind].__len__() == 1:
                    self.board_for_sure[coor] = self.possibilities[ind][0]
                    
                else:
                    # If the row/column/region only have 1 spot have the possibility,
                    # Update the value into the for_sure_board
                    for val in self.possibilities[ind]:
                        get_for_sure = False
                        for set_coor in self._get_set_coor(coor):
                            if self.check_num_poss(val, set_coor, ind) == 1:
                                self.board_for_sure[coor] = val
                                # print(self.board_for_sure)
                                self.check_possibiities_all_direction(print_board=True)
                                # print(self.possibilities)
                                get_for_sure = True
                            else:
                                pass
                        if get_for_sure == True:
                            break

    def eliminate_poss(self):
        # Create row, col and region objects
        all_objs = []
        for m in range(self.GRID_SIZE):
            # row
            all_objs.append([self.INDEX_REVERSE[m, j] for j in range(self.GRID_SIZE)])
            # col
            all_objs.append([self.INDEX_REVERSE[i, m] for i in range(self.GRID_SIZE)])
            # region
        for m, n in itertools.product(range(self.AREA_SIZE), range(self.AREA_SIZE)): 
            all_objs.append([self.INDEX_REVERSE[i,j] for i, j in itertools.product(range(3*m, 3*m+3), range(3*n, 3*n+3))])

        for obj in all_objs:
            lean_obj = [ind for ind in obj if self.possibilities[ind].__len__() != 1]
            if len(lean_obj) <= 2:
                continue
            else:
                combinations = []
                for l in range(2, len(lean_obj)):
                    combinations += list(itertools.combinations(lean_obj,l))
                for com in combinations:
                    all_poss = []
                    for ind in com:
                        all_poss += self.possibilities[ind]
                    if len(set(all_poss)) == len(com):
                        for ex_ind in [ind for ind in lean_obj if ind not in com]:
                            self.possibilities[ex_ind] = [num for num in self.possibilities[ex_ind] if num not in set(all_poss)]
                        break

    # @timeit
    def solve(self):
        hash_before = 0
        hash_after = 1
        num_iter = 0
        self.check_possibiities_all_direction()
        while hash_before != hash_after:
            hash_before = hash(tuple(self.board_for_sure.flatten()))
            for _ in range(1):
                self.check_possibiities_all_direction()
                self.update_board_for_sure()
                self.eliminate_poss()
                self.update_board_for_sure()
                num_iter += 1
            hash_after = hash(tuple(self.board_for_sure.flatten()))
        return super().solve()