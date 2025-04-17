import pygame, sys
import py.settings as settings
import pyttsx3
from py.chess import get_col_chess, get_tile_from_location, move, check_mate
from py.movement import move_manager

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

viewing_row = -1; viewing_col = -1 # for if the user is viewing the board
possible_moves = []

def displayBoard():
    pygame.draw.rect(SCREEN,LIGHTGREEN,(0,0,1920,1080)) # set background color
    pygame.draw.rect(SCREEN,BLACK,(350,130,820,820), width = 10) # set chessboard color
    global viewing_row; global viewing_col

    for r in range(8):
        global possible_moves
        
        for c in range(8):
            # to create the checkerboard pattern if r and c are both odd or both even color the tile tan         
            if ((r % 2 == 0) and (c % 2 == 0)) or ((r %2 == 1) and (c%2 == 1)):
                square = pygame.draw.rect(SCREEN, TAN, (360 + (r * 100), 140 + (c * 100), 100, 100), 0)
            else:
                square = pygame.draw.rect(SCREEN, BROWN, (360 + (r * 100), 140 + (c * 100), 100, 100), 0)

            if (viewing_row != -1 and viewing_col != -1) and c == viewing_row and r == viewing_col:
                pygame.draw.rect(SCREEN, YELLOW, (360 + (r * 100), 140 + (c * 100), 100, 100), 3) # if the player is currently 'viewing' a tile- add a boarder to it
                
            if settings.board[c][r] in possible_moves:
                pygame.draw.rect(SCREEN, BLUE, (360 + (r * 100), 140 + (c * 100), 100, 100), 3) # if a piece is able to move to this tile- add a boarder to it


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
    # if the user was going to go off the board the previous value will be read (since the users movement was prevented)

def read_off_list():
    global possible_moves
    
    for i in possible_moves:
        # if the side of the piece is not 'N' then there is a piece there
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
        else:
            # if the possible moves array is empty the player cannot move
            read("There are no possible places for this piece to move to")

# handles selecting where a piece can move to
def handle_moving_end(selected_piece, moving_to):
    global possible_moves
    
    start_tile = get_tile_from_location(selected_piece)
    end_tile = get_tile_from_location(moving_to)

    # if the new tile is one of the possible moves
    if get_tile_from_location(moving_to) in possible_moves:
        move(start_tile, end_tile)  # move the piece on the tile to the new tile

        #changes the turn
        if settings.turn == 'W':
            settings.turn = 'B'
        else:
            settings.turn = 'W'

        # confirm movement to player
        #read(f'{start_tile.location} {end_tile.piece.type} moving to {end_tile}')
        read("It is now the other player's turn")
    else:
        read(f'{moving_to} is an illegal move')

def key_react(key_value, selected_piece):
    # if the pressed key is between a-h and there is nothing in the current tile tracking
    if 97 <= int(key_value) <= 104 and len(selected_piece) == 0:
        selected_piece = chr(key_value)
    # if the pressed key is between 1-8 and a-h was selected before
    elif 49 <= int(key_value) <= 56 and len(selected_piece) == 1:
        selected_piece += chr(key_value)
            
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
        selected_piece = ""
    
    return selected_piece

def start_display():
    pygame.init() # initalizing pygame

    global SCREEN; global FONT; global PIECE_FONT; global possible_moves
    SCREEN = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    FONT = pygame.font.SysFont(None, 80)
    PIECE_FONT = pygame.font.Font("./assets/segoe-ui-symbol.ttf",80)
    
    selected_piece = "" # for if the user is trying to select a tile
    moving_to = "" # for if the user is trying to select a tile
    read = False

    # a pygame loop that runs while the user is playing
    while True:
        print("White" + str(check_mate('W')))
        print("Black" + str(check_mate('B')))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if len(selected_piece) != 2:
                    selected_piece = key_react(event.key, selected_piece)
                    
                elif len(moving_to) != 2:
                    moving_to = key_react(event.key, moving_to)
            
            if len(selected_piece) == 2 and not read:
                handle_moving_start(selected_piece)
                read = True
            elif len(moving_to) == 2:
                handle_moving_end(selected_piece, moving_to)
                possible_moves = []
                selected_piece = ""
                moving_to = ""
                    

        displayBoard() # display whats on the board
        displayColumns() # show column letters
        displayRows() # show row numbers
        pygame.display.flip() #update the board
