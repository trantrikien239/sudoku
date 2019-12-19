import numpy as np
import itertools

class Game:
    DUMMY_BACKGROUND = [[0] * 9] * 9
    DUMMY_REGION = [[[[0]*3] * 3] * 3] * 3
    AREA_SIZE = 3
    GRID_SIZE = AREA_SIZE * AREA_SIZE


    def __init__(self):
        self.board = np.array(self.DUMMY_BACKGROUND)

    def get_board_regions(self):
        regions = np.array(self.DUMMY_REGION)
        for i,j in itertools.product(range(self.AREA_SIZE), range(self.AREA_SIZE)):
            regions[i,j] = self.board[self.AREA_SIZE*i : self.AREA_SIZE*(i+1), self.AREA_SIZE*j : self.AREA_SIZE*(j+1)]
        return regions
            
    def load_puzzle(self, iterable_2d):
        for i,j in itertools.product(range(self.GRID_SIZE), range(self.GRID_SIZE)):
            self.board[i,j] = iterable_2d[i][j]

    def load_puzzle_from_file(self, file_path):
        pass


    @staticmethod
    def check_1to9(ndarray):
        if (sorted(ndarray.flatten()) == np.array([1,2,3,4,5,6,7,8,9])).all():
            return True
        else:
            return False

    def check_solution(self):
        CORRECT = True
        # check rows
        for i in range(self.GRID_SIZE):
            CORRECT = CORRECT & self.check_1to9(self.board[i,:])
        # check columns
        for i in range(self.GRID_SIZE):
            CORRECT = CORRECT & self.check_1to9(self.board[:,i])
        # check regions
        regions = self.get_board_regions()
        for i,j in itertools.product(range(self.AREA_SIZE), range(self.AREA_SIZE)):
            CORRECT = CORRECT & self.check_1to9(regions[i,j])
        
        return CORRECT

if __name__ == '__main__':
    game = Game()
    DATA = np.random.randint(0,9,size=(9,9))
    game.load_puzzle(DATA)
    print(game.board)
    print(game.check_solution())