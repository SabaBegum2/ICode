# importing the required libraries
import pygame as pg
import sys 
import time
from pygame.locals import *
# The sys module in Python provides access to system-specific parameters and functions. 
# It allows interaction with the Python interpreter and the operating system environment. 
 
# declaring the global variables
 
# for storing the 'x' or 'o'
# value as character
XO = 'x' #tracks the current players x or 0
 
# storing the winner's value at
# any instant of code
winner = None
 
# to check if the game is a draw
draw = None
 
# to set width of the game window
width = 400
 
# to set height of the game window
height = 400
 
# to set background color of the
# game window
white = (255, 255, 255)
 
# color of the straightlines on that
# white game board, dividing board
# into 9 parts
line_color = (0, 0, 0)
 
# setting up a 3 * 3 board in canvas
'''[none]represents a absense of value'''
board = [[None]*3, [None]*3, [None]*3]
 
 
# initializing the pygame window
pg.init()
 
# setting fps manually
#frames per second
'''FPS, or frames per second, refers to the number of frames 
a program renders in one second. In Python, it's commonly used 
in the context of game development or video processing to measure 
performance and smoothness of animations or videos.'''
fps = 30 
 
# this is used to track time
CLOCK = pg.time.Clock()
 
# this method is used to build the
# infrastructure of the display
'''display position'''
screen = pg.display.set_mode((width, height + 100), 0, 32)
 
# setting up a nametag for the
# game window
pg.display.set_caption("My Tic Tac Toe")
 
# loading the images as python 
'''Images are loaded as Python objects to enable manipulation and processing within Python's ecosystem. 
Image manipulation:
Resizing, cropping, rotating, and applying filters can be performed by directly modifying the pixel data within the array
'''
initiating_window = pg.image.load("modified_cover.png")
x_img = pg.image.load("X_modified.png")
y_img = pg.image.load("o_modified.png")
 
# resizing images
initiating_window = pg.transform.scale(
    initiating_window, (width, height + 100))
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(y_img, (80, 80))
 
 
'''displays the initial screen with the board layout'''
def game_initiating_window():
 
    # displaying over the screen
    screen.blit(initiating_window, (0, 0))
 
    # updating the display
    pg.display.update()
    time.sleep(3)
    screen.fill(white)
 
    # drawing vertical lines
    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(screen, line_color, (width / 3 * 2, 0),
                 (width / 3 * 2, height), 7)
 
    # drawing horizontal lines
    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, line_color, (0, height / 3 * 2),
                 (width, height / 3 * 2), 7)
    draw_status()
 
 
def draw_status():
    '''Displays the current game status: players turn, winners, or draw'''
    # getting the global variable draw
    # into action
    global draw
 
    if winner is None:
        message = XO.upper() + "'s Turn" #displays the current players turn
    else:
        message = winner.upper() + " won !" #displays the winning player
    if draw:
        message = "Game Draw !"
 
    # setting a font object
    '''defining the font setting'''
    font = pg.font.Font(None, 30)
 
    # setting the font properties like
    # color and width of the text
    text = font.render(message, 1, (255, 255, 255))
 
    # copy the rendered message onto the board
    # creating a small block at the bottom of the main display
    '''clear the status bar and display the message'''
    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width / 2, 500-50))
    screen.blit(text, text_rect)
    pg.display.update()
 
 
def check_win():
    '''checks if there is a winner or there is a draw'''
    global board, winner, draw
 
    # checking for winning rows
    for row in range(0, 3):
        if((board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None)):
            winner = board[row][0]
            pg.draw.line(screen, (250, 0, 0),
                         (0, (row + 1)*height / 3 - height / 6),
                         (width, (row + 1)*height / 3 - height / 6),
                         4)
            break
 
    # checking for winning columns
    for col in range(0, 3):
        if((board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None)):
            winner = board[0][col]
            pg.draw.line(screen, (250, 0, 0), ((col + 1) * width / 3 - width / 6, 0),
                         ((col + 1) * width / 3 - width / 6, height), 4)
            break
 
    # check for diagonal winners
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
 
        # game won diagonally left to right
        winner = board[0][0]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)
 
    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
 
        # game won diagonally right to left
        winner = board[0][2]
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)
 
    '''check if the board is full and no winner'''
    if(all([all(row) for row in board]) and winner is None):
        draw = True
    draw_status()
 

# place an x or 0 in the selected board cell 
def drawXO(row, col):
    global board, XO
 
    # for the first row, the image
    # should be pasted at a x coordinate
    # of 30 from the left margin

    '''calculating the positions for drawing the image'''
    if row == 1:
        posx = 30
 
    # for the second row, the image
    # should be pasted at a x coordinate
    # of 30 from the game line
    if row == 2:
 
        # margin or width / 3 + 30 from
        # the left margin of the window
        posx = width / 3 + 30
 
    if row == 3:
        posx = width / 3 * 2 + 30
 
    if col == 1:
        posy = 30
 
    if col == 2:
        posy = height / 3 + 30
 
    if col == 3:
        posy = height / 3 * 2 + 30
 
    # setting up the required board
    # value to display
    '''updating the board with the player moves'''
    board[row-1][col-1] = XO
 
    if(XO == 'x'):
 
        # pasting x_img over the screen
        # at a coordinate position of
        # (pos_y, posx) defined in the
        # above code
        screen.blit(x_img, (posy, posx))
        XO = 'o'
 
    else:
        screen.blit(o_img, (posy, posx))
        XO = 'x'
    pg.display.update()
 
 
def user_click():
    # get coordinates of mouse click
    '''handles user clicks to determine where to place 'x' or 'o'''
    x, y = pg.mouse.get_pos()
 
    # get column of mouse click (1-3)
    if(x < width / 3):
        col = 1
 
    elif (x < width / 3 * 2):
        col = 2
 
    elif(x < width):
        col = 3
 
    else:
        col = None
 
    # get row of mouse click (1-3)
    if(y < height / 3):
        row = 1
 
    elif (y < height / 3 * 2):
        row = 2
 
    elif(y < height):
        row = 3
 
    else:
        row = None
 
    # after getting the row and col,
    # we need to draw the images at
    # the desired positions
    if(row and col and board[row-1][col-1] is None):
        global XO
        drawXO(row, col)
        check_win()
 
'''resets the game after a win or a draw''' 
def reset_game():
    global board, winner, XO, draw
    time.sleep(3)
    XO = 'x'
    draw = False
    game_initiating_window()
    winner = None
    board = [[None]*3, [None]*3, [None]*3]
 
 
game_initiating_window()
 
'''game loop''' 
while(True):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            user_click()
            if(winner or draw):
                reset_game()
    pg.display.update()
    CLOCK.tick(fps)