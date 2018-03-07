"""
Clone of 2048 game.
"""

#import poc_2048_gui
#import user42_UQUAen09CY_3 as testSuite
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

# merge function to merge two identical numbers
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    res = [0] * len(line)
    res_index = 0
    previous_tile = -1
    
    # now, loop through line, and structure the return list
    for tile in line:
        if tile == previous_tile:
            res[res_index - 1] = tile * 2
            previous_tile = -1
        elif tile > 0:
            res[res_index] = tile
            previous_tile = tile
            res_index += 1
    return res

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        
        # Initialize class
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._cells = []
        self.reset()
        # create a dictionary that holds the initial indices for the move direction
        self._initials = {}
        self._initials[UP] = [(0,col)for col in range(grid_width)]
        self._initials[DOWN] = [(grid_height-1,col)for col in range(grid_width)]
        self._initials[LEFT] = [(row, 0) for row in range(grid_height)]
        self._initials[RIGHT] = [(row,grid_width-1) for row in range(grid_height)]
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        #intialize all the cells to 0
        self._cells = [[0 for dummy_col in range(self._grid_width)]
                            for dummy_row in range(self._grid_height)]
        #randomly place two tiles
        self.new_tile()
        self.new_tile()
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        #generate a two or four randomly (90% chance for 2, 10% chance for 4)
        #two_and_four = [4,2,2,2,2,2,2,2,2,2]
        #random_two_four = two_and_four[random.randrange(10)]
        random_two_four = random.random()
        if random_two_four < 0.1:
            two_or_four = 4
        else:
            two_or_four = 2
        
        #place that two or four in a randomly selected empty cell if exists
        empty_cell = False
        avail_cells = []
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if self._cells[row][col] == 0:
                    empty_cell = True
                    avail_cells.append([row, col])
        if empty_cell == True:
            random_cell = random.choice(avail_cells)
            self._cells[random_cell[0]][random_cell[1]] = two_or_four
        

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        res = ""
        for row in range(self._grid_height):
            if row < self._grid_height -1:
                res += str(self._cells[row]) + ","
            else:
                res += str(self._cells[row])
        return res
    
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        index_list = self._initials[direction]
        
        if direction == UP or direction == DOWN:
            iter_range = self._grid_height
        elif direction == LEFT or direction == RIGHT:
            iter_range = self._grid_width
            
        tile_changed = False
       
        for item in index_list:
            # add the numbers to the temp_list then merge the list
            temp_list = []
            for row in range(iter_range):
                next_row = item[0]+ row * OFFSETS[direction][0]
                next_col = item[1] + row * OFFSETS[direction][1]
                temp_list.append(self.get_tile(next_row,next_col))
            # merge list
            new_list = merge(temp_list)    
            # put the new values back to the grid
            for row in range(iter_range):
                next_row = item[0]+ row * OFFSETS[direction][0]
                next_col = item[1] + row * OFFSETS[direction][1]
                if self._cells[next_row][next_col] != new_list[row]:
                    tile_changed = True
                self.set_tile(next_row,next_col,new_list[row])
        if tile_changed == True:
            self.new_tile()
    

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._cells[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._cells[row][col]

#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

# test merge function
#testSuite.run_merge_test(merge)

# test init
#testGame = TwentyFortyEight(5, 4)
#print(testGame._grid_height)
#print(testGame._grid_width)
# test __str__
#print(testGame)
# test set_tile
#testGame.set_tile(0, 0, 5)
#print(testGame._cells[0][0])
# test the initial indices
#print testGame.init_indices
