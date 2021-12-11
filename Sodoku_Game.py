# GUI.py
import pygame
import time
from tkinter import *
from tkinter import messagebox

pygame.font.init()

root = Tk() 

# Testing board:
board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

# Function to print a board:
def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:   # If row (i) is a factor of 3 then print lines before the numbers
            print("- - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:   # If column (j) is a factor of 3 then print lines before 
                print(" | ", end = "")    # inserted the end = "" to change default of new line to no space

            if j == 8:  # Check if we are at last position
                print(bo[i][j]) # if we are at last position then we print with new line after
            else:
                print(str(bo[i][j]) + " ", end="")  # If we are not at the last position then we print without new line after


def find_empty(board):  # Find empty position in board
    for i in range(len(board)):
        for j in range (len(board[0])):
            if board[i][j] == 0:
                return(i, j)    # Return tuple of (row, col)
    
    return None


def valid(board, number, pos):  # For given number and position, check if number valid in position
    # Need to check row, col, square
    # pos[0] = row and pos[1] = column

    # Check row
    for i in range(len(board[0])):  # Go through columns
        if board[pos[0]][i] == number and pos[1] != i:  # Check rows except where we inserted
            return False
        
    # Check col
    for i in range(len(board)):
        if board[i][pos[1]] == number and pos[0] != i:  # Check columns except where we inserted 
            return False

    # Check square

    box_x = pos[1] // 3     # 0, 1, 2 for box rows
    box_y = pos[0] // 3     # 0, 1, 2 for box columns

    for i in range(box_y *3, box_y *3  + 3):    # convert from 0, 1, 2 back to 0 to 9
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == number and (i, j) != pos:  # Check if number is in the box exccliding the numner itself
                return False

    return True # If we don't return false then the position is valid.\


def solve(board):   # Recursive function that calls itself

    find = find_empty(board)    # Get first available empty position

    if not find:    
        return True     # We found a solution thus no empty positions left  (We are done!)
    else:
        row, col = find     # Get available row and column from find tuple
    
    for i in range(1, 10):  # loop through numbers 1 to 9
        if valid(board, i, (row, col)):
            board[row][col]  = i    # Add number to board if valid

            if solve(board):    # Recursively call solve function 
                return True

            board[row][col] = 0     # Backtrack and set last value to 0 and try process again
        
    return False    # If we looped trough all of the numbers and all not valid then return false
        

# print_board(board)
# print("\n")
# solve(board)
# print_board(board)


class Grid: # Grid class to hold multiple cubes

    def __init__(self, rows, cols, width, height, board):
        self.board = board
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]  # Place a cube at position i, j while looping through the rows and columns
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def update_model(self):     # Board in the background want to check if final values placed is solvable (Multiple solutions possible so check if final values inserted produce valid solution)
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):   # Try to place perminant value and make sure it is valid to place in selected place
        row, col = self.selected
        if self.cubes[row][col].value == 0: # If selected cube has value of 0
            self.cubes[row][col].set(val)   # Set final value
            self.update_model()     # Update model 

            if valid(self.model, val, (row,col)) and solve(self.model): # Check if valid
                return True
            else:   # Else clear value and reset model
                self.cubes[row][col].set(0) 
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):  # Set temp value for cube object (Pencil)
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):    # Draw grid lines and cubes
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):     # Select block to let cube update border
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):    # Clear the block value when delete button cleared
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):   # Return the position of the cubed clicked on

        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))  # Return row and colomn of selected cube
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cube:     # The grid class holds multiple cubes
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value  # Actaul value that is final and can't be changed
        self.temp = 0   # Default temp value that gets "Penciled" in
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False   # Default value for selected state

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)  # Import python font

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:  # If temp value inserted and final value not been selected then place temp value
            text = fnt.render(str(self.temp), 1, (128,128,128))     # Text for block with temp value 
            win.blit(text, (x+5, y+5))  # Place text on window (block)
        elif not(self.value == 0):  # If final values has not been placed then place final value
            text = fnt.render(str(self.value), 1, (0, 0, 0))    # Text for block with final value
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))   # Place text on window (block)

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)    #If selected then draw lock on the outside

    def set(self, val):     # For setting final value
        self.value = val

    def set_temp(self, val):    # For setting penciled value
        self.temp = val


def redraw_window(win, board, time, strikes):   # Redraw window but with updated time and strikes
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 35)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))     # Text for current time
    win.blit(text, (540 - 175, 545))    # Place time text
    # Draw Strikes
    if strikes < 10:
        text = fnt.render("X " * strikes, 1, (255, 0, 0))   # Text for strike
        win.blit(text, (20, 545))   # Place strike
    # Draw grid and board
    board.draw(win)     # Draw window


def format_time(secs):  # Format the time into correct sting format
    sec = secs%60
    minute = secs//60
    myString = " " + str(minute) + ":" + str(sec)
    return myString


def main():
    global board

    # Window setup:
    win = pygame.display.set_mode((540,600)) 
    pygame.display.set_caption("Sudoku")

    board_grid = Grid(9, 9, 540, 540, board) # draw the board grid with 9 rows and columns with size 540x540 with the board as input
    key = None
    run = True 
    start_time = time.time() # Time when game started
    strikes = 0 # Reset the strikes'

    while run:

        cur_time = round(time.time() - start_time)  # Update timer

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # If quit pressed then stop the game
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: # If press 1 to 9 then fill in the box
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9

                if event.key == pygame.K_DELETE:    # If press clear then clear the box 
                    board_grid.clear()
                    key = None
                    
                if event.key == pygame.K_RETURN:    # If enter key pressed then check if value entered is correct
                    i, j = board_grid.selected   #Get the position selected
                    if board_grid.cubes[i][j].temp != 0 and board_grid.cubes[i][j].temp != board_grid.cubes[i][j].value:     # If there is a temp value entered and that is has not already been entered correctly (Can't lose if already won)
                        if board_grid.place(board_grid.cubes[i][j].temp): # Check if the tmep value can be placed without error and placed perminantly
                            print("Success")    # Success if the value can be placed
                        else:   # Else wrong and increase strikes
                            strikes += 1 
                            print("Wrong")
                            if strikes == 10:
                                root.withdraw() # Need to draw root tkinter window so that messagebox don't open it
                                messagebox.showerror(title = None, message = "You Lose !")
                                root.destroy()
                                run = False  
                        key = None  

                        if board_grid.is_finished():
                            print("Game over")
                            run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board_grid.click(pos)
                if clicked:
                    board_grid.select(clicked[0], clicked[1])
                    key = None

        if board_grid.selected and key != None:  # If selected box and no number has been inserted, then draw number
            board_grid.sketch(key)

        redraw_window(win, board_grid, cur_time, strikes)    # Update window wth new time and status
        pygame.display.update()


main()
pygame.quit()