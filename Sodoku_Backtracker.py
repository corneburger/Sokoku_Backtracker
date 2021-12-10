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
        

print_board(board)
print("\n")
solve(board)
print_board(board)