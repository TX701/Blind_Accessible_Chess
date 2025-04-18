import pygame, sys
import py.settings as settings
import pyttsx3
from py.chess import *
from py.movement import move_manager
import py.engine as sieng

# constant color values
WHITE = (255,255,255)
BROWN = (180,135,100)
TAN = (240,216,181)
LIGHTGREEN = (67,93,73)
BLACK = (0,0,0)
YELLOW = (255,255,143)
BLUE = (30,144,255)

# determing size and fonts
WINDOW_SIZE = (1920, 1000) 
SCREEN = None
FONT = None
PIECE_FONT = None

engine = pyttsx3.init()

possible_moves = []
viewing_row = -1; viewing_col = -1 # for if the user is viewing the board

def displayBoard():
    pygame.draw.rect(SCREEN,LIGHTGREEN,(0,0,1920,1080)) # set background color
    pygame.draw.rect(SCREEN,BLACK,(350,130,820,820), width = 10) # set chessboard color

    global viewing_row; global viewing_col
    
    for r in range(8):
        for c in range(8):
            # to create the checkerboard pattern if r and c are both odd or both even color the tile tan
            if ((r % 2 == 0) and (c % 2 == 0)) or ((r % 2 == 1) and (c % 2 == 1)):
                square = pygame.draw.rect(SCREEN, TAN, (360 + (r * 100), 140 + (c * 100), 100, 100))
            else:
                square = pygame.draw.rect(SCREEN, BROWN, (360 + (r * 100), 140 + (c * 100), 100, 100))

            if (viewing_row != -1 and viewing_col != -1) and c == viewing_row and r == viewing_col:
                pygame.draw.rect(SCREEN, YELLOW, (360 + (r * 100), 140 + (c * 100), 100, 100), 3) # if the player is currently 'viewing' a tile- add a boarder to it

            # if settings.board[c][r] in possible_moves:
            #     pygame.draw.rect(SCREEN, BLUE, (360 + (r * 100), 140 + (c * 100), 100, 100), 3) # if the player is currently 'viewing' a tile- add a boarder to it

            # set the text on the tile to be the current piece that is in that spot on the board
            text = PIECE_FONT.render(settings.board[c][r].piece.name, True, (0, 0, 0)) 
            rect = text.get_rect(center = (square.centerx, square.centery)) # places text in the middle of the square
            SCREEN.blit(text, rect)

# A-H display on top
def displayColumns():
    width = 410
    for i in range(1, 9):
        row = FONT.render(get_col_chess(i - 1), True, BLACK)
        w,h = FONT.size(get_col_chess(i))
        SCREEN.blit(row,(width-w,110-(h/2)))
        width += 100

# 1-8 display on left
def displayRows():
    height = 190
    for i in range(1, 9):
        row = FONT.render(str(9-i), True, BLACK)
        w,h = FONT.size(str(9-i))
        SCREEN.blit(row,(325-w,height-(h/2)))
        height += 100

# reads out given text with the text to speech
def read(text):
    # engine.setProperty('rate', 400)  #change this to be slower, this is just for my sanity rn
    engine.say(text)
    engine.runAndWait()
    engine.stop()


# reads off whos turn its is currently
def turn_update():
    current_turn = "White" if settings.turn == "W" else "Black"
    read(f'{current_turn}\'s turn')

# for given a row and col return whats on the board in that location
# used for the player to visualize whats on the board
def get_information():
    global viewing_row; global viewing_col

    location = f'{chr(viewing_col + 65)}{8 - viewing_row }'
    type = settings.board[viewing_row][viewing_col].piece.type
    side = "Black" if settings.board[viewing_row][viewing_col].piece.side == "B" else "White"
    side_type = "nothing" if type == None else f'a {side} {type}'

    read(f'{location} contains {side_type}')

# so the arrow keys can be used to move around the board and read off whats on each tile
def handle_arrow_view(type):
    global viewing_row; global viewing_col

    if viewing_row == -1 or viewing_col == -1:
        # if the player has not used the arrow keys yet start them in the top left corner
        viewing_row = 0; viewing_col = 0 
    elif (type == "U"):
        # if the player is not going to go off the board move them one up
        viewing_row = viewing_row - 1 if viewing_row != 0 else viewing_row
    elif (type == "R"):
        # if the player is not going to go off the board move them one to the right
        viewing_col = viewing_col + 1 if viewing_col != 7 else viewing_col
    elif (type == "D"):
        # if the player is not going to go off the board move them one down
        viewing_row = viewing_row + 1 if viewing_row != 7 else viewing_row
    elif (type == "L"):
        # if the player is not going to go off the board move them one to the left
        viewing_col = viewing_col - 1 if viewing_col != 0 else viewing_col
        
    get_information() # return what the given row col contains

def read_off_list():
    global possible_moves

    for i in possible_moves:
        # if the side of the piece is not 'N' then there is a piece there
        for event in pygame.event.get():
             # if the user pressed a key
            if event.type == pygame.KEYDOWN:
                if event.key == 113:
                    return None

        if (i.piece.side != 'N'):
            side = "Black" if i.piece.side == "B" else "White"
            read(f'{i.location} {side} {i.piece.type}') # read location side and piece
        else: read(i.location) # if there is no piece just read the location

# if the user has typed in a row col combination
def handle_moving_start(current_tile):
    global possible_moves
    tile = get_tile_from_location(current_tile) # gets what is on that tile

    # if there are no pieces on the given tile, the player cannot move
    if tile.piece.type == None:
        read("There are no pieces on this tile")
    elif tile.piece.side != settings.turn:
        read("This is the opponent's piece, you are not allowed to move it") 
    else:
        side = "Black" if tile.piece.side == "B" else "White" if tile.piece.side == "W" else ""
        read(f'Selected {current_tile} {side} {tile.piece.type}') # reads off the location color and piece
        possible_moves = move_manager(tile) # gets where the piece on the given tile can move to
    
        if len(possible_moves) > 0:
            read("The piece on this tile can move to")
            read_off_list()

            handle_moving_end(tile) # start checking for where to move to
        else:
            # if the possible moves array is empty the player cannot move
            read("There are no possible places for this piece to move to")

# handles selecting where a piece can move to
def handle_moving_end(tile_to_move):
    global possible_moves
    waiting = True # waiting for the users input
    current_tile = "" # a chess location A8 C4 etc

    while(waiting):
        for event in pygame.event.get():
             # if the user pressed a key
            if event.type == pygame.KEYDOWN:
                key_value = event.key
                # if the pressed key is between a-h and there is nothing in the current tile tracking
                if 97 <= int(key_value) <= 104 and len(current_tile) == 0:
                    current_tile = chr(key_value)
                # if the pressed key is between 1-8 and a-h was selected before
                elif 49 <= int(key_value) <= 56 and len(current_tile) == 1:
                    current_tile += chr(key_value)

                    # if the new tile is one of the possible moves
                    if get_tile_from_location(current_tile) in possible_moves:
                        move(tile_to_move, get_tile_from_location(current_tile))  # move the piece on the tile to the new tile
                        pygame.display.flip() #update the board
                        # confirm movement to player
                        read(f'{tile_to_move.location} {get_tile_from_location(current_tile).piece.type} moving to {current_tile}')
                        read("It is now the other player's turn")
                    else:
                        read(f'{current_tile} is an illegal move')

                    current_tile = ""
                    waiting = False

                # pressed 'r'
                elif int(key_value) == 114:
                    read_off_list()

def handle_presses(key_value, current_tile):
    # if the pressed key is between a-h and there is nothing in the current tile tracking
    if 97 <= int(key_value) <= 104 and len(current_tile) == 0:
        current_tile = chr(key_value)
    # if the pressed key is between 1-8 and a-h was selected before
    elif 49 <= int(key_value) <= 56 and len(current_tile) == 1:
        current_tile += chr(key_value)
        handle_moving_start(current_tile) # we have a chess location and will start the move process
        current_tile = "" # reset current tile

    elif key_value == pygame.K_UP:
        # the player has moved their 'visual' adjust row col
        handle_arrow_view("U")
    elif key_value == pygame.K_RIGHT:
        # the player has moved their 'visual' adjust row col
        handle_arrow_view("R")
    elif key_value == pygame.K_DOWN:
        # the player has moved their 'visual' adjust row col
        handle_arrow_view("D")
    elif key_value == pygame.K_LEFT:
        # the player has moved their 'visual' adjust row col
        handle_arrow_view("L")
    else: 
        current_tile = ""
    
    return current_tile

def start_display():
    global viewing_row; global viewing_col; global SCREEN; global FONT; global PIECE_FONT
    pygame.init() # initalizing pygame

    # determing size and fonts
    SCREEN = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    FONT = pygame.font.SysFont(None, 80)
    PIECE_FONT = pygame.font.Font("./assets/segoe-ui-symbol.ttf",80)
    
    current_tile = "" # for if the user is trying to select a tile

    # a pygame loop that runs while the user is playing
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # if is_in_check(settings.player_color):
            #     read("you are in check")
            # if is_in_check(settings.eng.side):
            #     read("opponent is in check")

            if settings.turn != settings.player_color:
                sieng.rand_move(settings.eng) # now let the engine make a move

            # if the user pressed a key
            elif event.type == pygame.KEYDOWN:
                current_tile = handle_presses(event.key, current_tile)

            displayBoard() # display whats on the board
            displayColumns() # show column letters
            displayRows() # show row numbers
            pygame.display.flip() #update the board
