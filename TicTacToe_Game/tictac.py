# -----------------------------------------------------------------------------
# Purpose:    Implement a game of Tic Tac Toe
# -----------------------------------------------------------------------------
'''
Module to play a tic-tac-toe game

It is a 3 X 3 game. Human player always gets to play first, the computer player.
The player who succeeds in placing three marks in a horizontal, vertical, 
or diagonal row wins the game.
'''
import tkinter
import random

class Game(object):
    '''
    Represent a tic-tac-toe game
    
    Arguments:
    parent: root window 
    
    Attributes:
    parent: root window
    '''

    # Add class variables if needed here - square size, etc...)
    # each square is 150 X 150
    square_size = 150 
    # set colors for the board, human player, and computer player
    org_color = 'green'
    human_color = 'pink'
    com_color = 'red'
    

    def __init__(self, parent):
        """
        Initialize the original state of the Game object:
            set the root window title
            create a restart button
            create a canvas
            create 3X3 rectangles on canvas, and set to original color
            bind canvas click event handler
            create a label to display game status message
            set continue_play to True
            set the original state of the 3X3 board
        
        Parameters:
            parent - root window
        """
        parent.title('Tic Tac Toe')
        self.parent = parent
        # Create the restart button widget
        restart = tkinter.Button(parent, text='RESTART', command=self.restart)
        restart.grid()
        # Create a canvas widget
        self.canvas = tkinter.Canvas(parent, width=450, height=450, background=self.org_color)
        # self.canvas.grid()
        for row in range(3):
            for column in range(3):
                self.canvas.create_rectangle(self.square_size * column,
                                             self.square_size * row,
                                             self.square_size * (column + 1),
                                             self.square_size * (row + 1),
                                             fill=self.org_color)
                                            
        self.canvas.grid()
        
        # when the user clicks on the canvas, we invoke self.play
        self.canvas.bind("<Button-1>", self.play)
        
        
        # Create a label widget for the win/lose message
        self.result = tkinter.Label(parent, text='') 
        self.result.grid()
                     
        # Create any additional instance variable you need for the game
        self.continue_play = True # original state of continue_play is set to True
        # the original state of the board, represented in color green
        #it is a 3 x 3 list, two dimentional, each cell has has a position of [row][col]
        self.board = [['green', 'green', 'green'],
             ['green', 'green', 'green'],
             ['green', 'green', 'green']
            ]
     
       
        
    def restart(self):
        """
        This method is invoked when the user clicks on the RESTART button.
        
        Parameter:
            None
        Return:
            None
        
        Reset to the original state of the Game object:
            
            redraw 3X3 rectangles on canvas, and set to original color
            set continue_play to True
            set the original state of the 3X3 board
            reset the continue_play flag and label
        """
       
        for row in range(3):
            for column in range(3):
                self.canvas.create_rectangle(self.square_size * column,
                                             self.square_size * row,
                                             self.square_size * (column + 1),
                                             self.square_size * (row + 1),
                                             fill='green')
        # reset the board state
        self.board = [['green', 'green', 'green'],
                      ['green', 'green', 'green'],
                      ['green', 'green', 'green']
                     ]
        # reset the flag and label
        self.continue_play = True
        self.result.configure(text="")
             
             
    def play(self, event):
        """
        This method is invoked when the user clicks on a square.
        
        Parameters:
            event (when user clicks on the board)
        Return:
            None
            
        if continue_play flag is True:
            change the color to human color where human clicks
            change the board state
            check whether human won
            if not, check if it is a tie
            if not a tie or human won, let computer randomly pick a cell
            check whether computer won
            if not, check if it is a tie
        """
        
        if (self.continue_play == True):
            square = self.canvas.find_closest(event.x, event.y)
            #change the color display for the cell
            self.canvas.itemconfigure(square, fill=self.human_color)
            # change the board state
            new_col = event.x // self.square_size
            new_row = event.y // self.square_size
            if (self.board[new_row][new_col] == self.org_color):
                self.board[new_row][new_col] = self.human_color
            
            # now, determine the state of the game, win or tie
            self.isWin('pink', new_row, new_col)
            # if it is a tie 
            if (self.continue_play == True):
                if (self.isFull() == True):
                    self.result.configure(text="It's a tie!")                
            
            # computer plays 
            if (self.continue_play == True):
                com_row = random.randint(0,2)
                com_col = random.randint(0,2)
                while (self.board[com_row][com_col] != self.org_color):
                    com_row = random.randint(0,2)
                    com_col = random.randint(0,2)
               
                self.board[com_row][com_col] = self.com_color
                square = self.canvas.find_closest(self.square_size * com_col, 
                                                  self.square_size * com_row)
            
                self.canvas.itemconfigure(square, fill=self.com_color)
                # check if computer won
                self.isWin('red', com_row, com_col) 
                # if it is a tie 
                if (self.continue_play == True):
                    if (self.isFull() == True):
                        self.result.configure(text="It's a tie!")  
            # this is for debug only   
            #print ("new grid here: ")    
            #print (self.board)
            #print ("----------------")
                        
        
    def isWin(self, color, row, col):
        """
        This method checks whether the player won or lost
        
        Paramters:
            color (string): orig_color, human_color, or com_color
            row (int): 0-2, represents the row num of the cell
            col (int): 0-2, represents the col num of the cell
        Return:
            None
        
        check if the player won (horizonally)
        else check if player won (vertically)
        else check if player won (diagonally): two possibilities
        while checking the above, if computer won, then human lost
        
        Note: It can be modified to accomodate 4X4, 5X5, etc, will then 
        use two counters, to loop through rows or cols, and check for values
        In this case, since there are only 3X3, I just hard-coded 
        """
        if (self.board[row][0] == color and 
            self.board[row][1] == color and
            self.board[row][2] == color):
                if (color == self.com_color):
                     self.result.configure(text="You lost!")
                else:
                     self.result.configure(text="You won!")
                self.continue_play = False 
        elif (self.board[0][col] == color and 
             self.board[1][col] == color and
             self.board[2][col] == color):
                 if (color == self.com_color):
                     self.result.configure(text="You lost!")
                 else:
                     self.result.configure(text="You won!")
                 self.continue_play = False 
        elif (self.board[2][0] == color and 
              self.board[1][1] == color and
              self.board[0][2] == color):
                 if (color == self.com_color):
                     self.result.configure(text="You lost!")
                 else:
                     self.result.configure(text="You won!")
                 self.continue_play = False 
        elif (self.board[0][0] == color and 
              self.board[1][1] == color and
              self.board[2][2] == color):
                 if (color == self.com_color):
                     self.result.configure(text="You lost!")
                 else:
                     self.result.configure(text="You won!")
                 self.continue_play = False 
                  
        
    def isFull(self):
        """
        This method checks whether all cells on the board are clicked
        
        Parameters:
            None
        Return:
            True or False
            
        if all cells have changed color (means they have been clicked)
        then the board is full, return True
        else it's not full, return False
        
        """
        filled = 0
        for row in range(3):
            for col in range(3):
                if (self.board[row][col] != self.org_color):
                    filled += 1
        if (filled == 9):
            self.continue_play = False
            #self.result.configure(text="It's a tie!")
            return True
        else:
            self.continue_play = True
            return False
        
        
    
def main():
    """
    main() method for this game
        
    """
    # Instantiate a root window
    root = tkinter.Tk() # make sure k is lower case
    
    # Instantiate a Game object
    game = Game(root)
    # Enter the main event loop
    root.mainloop()
    

if __name__ == '__main__':
    main()