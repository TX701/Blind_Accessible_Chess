import pygame, sys
import py.settings as settings
import pyttsx3
from py.chess import *
from py.check import *
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
#WINDOW_SIZE = (400, 1000) 
#USR_X = 1920
#USR_Y = 1000
SCREEN = None
FONT = None
PIECE_FONT = None

engine = pyttsx3.init()
possible_moves = []
viewing_row = None; viewing_col = None # for if the user is viewing the board
game_over = False
voice_rate = 200
opponent = None

#Sam's Global Vars
logArray = []
curLog = 0

# Method to display the board.
def displayBoard():
    #initializing some usr scren size dependent variables.
    USR_X,USR_Y = WINDOW_SIZE
    boardX = (360/1920) * USR_X
    boardY = (140/1080) * USR_Y
    tileX = (100/1920) * USR_X
    tileY = (100/1080) * USR_Y

    #Drawing background and board border.
    pygame.draw.rect(SCREEN,LIGHTGREEN,((0,0),WINDOW_SIZE)) # set background color
    pygame.draw.rect(SCREEN,BLACK,(boardX-10,boardY-10,((800/1920)*USR_X)+20,((800/1080)*USR_Y)+20), width = 10) # set chessboard color

    global viewing_row; global viewing_col
    
    
    for r in range(8):
        for c in range(8):
            # to create the checkerboard pattern if r and c are both odd or both even color the tile tan
            if ((r % 2 == 0) and (c % 2 == 0)) or ((r % 2 == 1) and (c % 2 == 1)):
                square = pygame.draw.rect(SCREEN, TAN, (boardX + (r * tileX), boardY + (c * tileY), tileX, tileY))
            else:
                square = pygame.draw.rect(SCREEN, BROWN, (boardX + (r * tileX), boardY + (c * tileY), tileX, tileY))

            if (viewing_row != -1 and viewing_col != -1) and c == viewing_row and r == viewing_col:
                pygame.draw.rect(SCREEN, YELLOW, (boardX + (r * tileX), boardY + (c * tileY), tileX, tileY), 3) # if the player is currently 'viewing' a tile- add a boarder to it

            if settings.board[c][r] in possible_moves:
                pygame.draw.rect(SCREEN, BLUE, (boardX + (r * tileX), boardY + (c * tileY), tileX, tileY), 3) # if the selected piece can move to a tile- add a boarder to it

            # set the text on the tile to be the current piece that is in that spot on the board
            text = PIECE_FONT.render(settings.board[c][r].piece.name, True, (0, 0, 0)) 
            rect = text.get_rect(center = (square.centerx, square.centery)) # places text in the middle of the square
            SCREEN.blit(text, rect)

# A-H display on top
def displayColumns():
    USR_X, USR_Y = WINDOW_SIZE
    width = ((360/1920)*USR_X) + ((50/1920)*USR_X)
    for i in range(1, 9):
        row = FONT.render(get_col_chess(i - 1), True, BLACK)
        w,h = FONT.size(get_col_chess(i))
        SCREEN.blit(row,(width-(w/2),((110/1080)*USR_Y)-h))
        width += ((100/1920)*USR_X)

# 1-8 display on left
def displayRows():
    USR_X, USR_Y = WINDOW_SIZE
    height = ((140/1080)*USR_Y) + ((50/1080)*USR_Y)
    for i in range(1, 9):
        row = FONT.render(str(9-i), True, BLACK)
        w,h = FONT.size(str(9-i))
        SCREEN.blit(row,(((325/1920)*USR_X)-w,height-(h/2)))
        height += ((100/1080)*USR_Y)

# Log Display
def displayLog():
    global logArray

    #Creating special font for log
    logFont = pygame.font.SysFont(None,30)

    #Initializing some variables that are dependent on users screen size.
    USR_X, USR_Y = WINDOW_SIZE
    LogX = (1340/1920)*USR_X
    LogY = (140/1080)*USR_Y
    LogW = (400/1920)*USR_X
    LogH = (800/1080)*USR_Y
    offset = (100/1080) * USR_Y

    #Drawing Log Background
    pygame.draw.rect(SCREEN,BLACK,(LogX-10,LogY-10,LogW+20,LogH+20),width = 10)
    pygame.draw.rect(SCREEN,WHITE,(LogX,LogY,LogW,LogH))

    #Printing last seven movements.
    if len(logArray) <= 7:
        for i in range(len(logArray)):
            log = logFont.render(logArray[i],True,BLACK)
            w,h = logFont.size(logArray[i])
            SCREEN.blit(log,(LogX + 15,(LogY+LogH) - ((i+1)*offset) - h/2))
    else:
        #A complicated way of trying to print the three logs "above" the curLog and the three logs "below" the current log.
        height = 0
        if (len(logArray) - 1 - curLog) >= 3:
            t = 3
        else:
            t = len(logArray) - 1 - curLog
        if (curLog >= 3):
            b = -3
        else:
            b = 0 - curLog
        for i in range (t,b,-1):
            log = logFont.render(logArray[curLog + i],True,BLACK)
            w,h = logFont.size(logArray[curLog + i])
            SCREEN.blit(log,(LogX + 15,(LogY+offset) + height - h/2))
            height += 100


# log recording module.
def logRecord(text):
    global logArray; global curLog

    logArray.append(text)

# log movement handling module
def handle_log(type):
    global logArray; global curLog
    if len(logArray) == 0:
        read("No logs to change or read")
        return

    if len(logArray) == 1:
        read(f"Reading only log")
        read(logArray[curLog])
        return

    if type == "up" and curLog == (len(logArray)-1):
        curLog += 1
        read(f"Reading log {curLog+1}")
        read(logArray[curLog])
        return
    elif type == "down" and curLog > 0:
        curLog -= 1
        read(f"Reading log {curLog+1}")
        read(logArray[curLog])
        return
    else:
        read("Cannot find further logs.")
        return


# reads out given text with the text to speech
def read(text):
    global voice_rate
    
    engine.setProperty('rate', voice_rate)  #change this to be slower later
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# reads off whos turn its is currently
def turn_update():
    current_turn = "White" if settings.turn == "W" else "Black"
    read(f'{current_turn}\'s turn')
    
def tile_to_side(tile):
   return "Black" if tile.piece.side == "B" else "White" if tile.piece.side == "W" else ""

# for given a row and col return whats on the board in that location
# used for the player to visualize whats on the board
def get_information():
    global viewing_row; global viewing_col

    if -1 < viewing_row and viewing_row < 8 and -1 < viewing_col and viewing_col < 8:
        location = f'{chr(viewing_col + 65)}{8 - viewing_row }'
        type = settings.board[viewing_row][viewing_col].piece.type
        side_type = "nothing" if type == None else f'a {tile_to_side(settings.board[viewing_row][viewing_col])} {type}'

        read(f'{location} contains {side_type}')
        
        if settings.board[viewing_row][viewing_col] in possible_moves:
            read("This is a possible move")
    else: 
        read("You are off the board")
        
        if viewing_row < 0:
            read("Move down to return to the board")
        elif viewing_col < 0:
            read("Move right to return to the board")
        elif 7 < viewing_row:
            read("Move up to return to the board")
        elif 7 < viewing_col:
            read("Move left to return to the board")
            
def read_board():
    for row in range(len(settings.board)):
        for col in range(len(settings.board[row])):
            for event in pygame.event.get():
                # if the user pressed q
                if event.type == pygame.KEYDOWN:
                    if event.key == 113:
                        return None
                
            tile = settings.board[row][col]
            text = f'{tile.location} nothing' if tile.piece.type == None else f'{tile.location} {tile_to_side(tile)} {tile.piece.type}'
            read(text)

# so the arrow keys can be used to move around the board and read off whats on each tile
def handle_arrow_view(type):
    global viewing_row; global viewing_col

    if viewing_row == None or viewing_col == None:
        # if the player has not used the arrow keys yet start them in the top left corner
        viewing_row = 0; viewing_col = 0 
    elif (type == "U"):
        # if the player is not going to go off the board move them one up
        viewing_row = viewing_row - 1 if viewing_row != -1 else viewing_row
    elif (type == "R"):
        # if the player is not going to go off the board move them one to the right
        viewing_col = viewing_col + 1 if viewing_col != 8 else viewing_col
    elif (type == "D"):
        # if the player is not going to go off the board move them one down
        viewing_row = viewing_row + 1 if viewing_row != 8 else viewing_row
    elif (type == "L"):
        # if the player is not going to go off the board move them one to the left
        viewing_col = viewing_col - 1 if viewing_col != -1 else viewing_col
        
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
            read(f'{i.location} {tile_to_side(i)} {i.piece.type}') # read location side and piece
        else: read(i.location) # if there is no piece just read the location
        
def read_off_controls():
    text = "To move a piece- enter that pieces location (ie A6), afterwards you will be told if you can move it or not.\n" \
            + "If you can, enter in another location to move the piece\n" \
            + "When selecting a piece to move, all its possible moves will be listed out. you can press Q to interrupt this list\n" \
            + "You can use the arrow keys to move around the board and hear what is on each tile\n" \
            + "You can press M to read off the entire board. you can press Q to stop reading\n" \
            + "You can press question to read off all possible moves you can make. you can press Q to stop reading\n" \
            + "You can press 0 to restart the game\n" \
            + "Press minus to decrease speech spead\n" \
            + "Press plus to increase speech spead"
            
    lines = text.split("\n")
    
    for line in lines:
        for event in pygame.event.get():
             # if the user pressed a key
            if event.type == pygame.KEYDOWN:
                if event.key == 113:
                    return None    
        read(line)
        
def all_moves(side):
    text = list_all_possible_moves(side)
    lines = text.split("\n")
    
    for line in lines:
        for event in pygame.event.get():
             # if the user pressed a key
            if event.type == pygame.KEYDOWN:
                if event.key == 113:
                    return None    
        read(line)
    
# if the user has typed in a row col combination
def handle_moving_start(tile_to_move):
    global possible_moves
    tile = get_tile_from_location(tile_to_move) # gets what is on that tile

    # if there are no pieces on the given tile, the player cannot move
    if tile.piece.type == None:
        read("There are no pieces on this tile" + str(tile.location))
    elif tile.piece.side != settings.turn:
        read("This is the opponent's piece, you are not allowed to move it") 
    else:
        read(f'Selected {tile_to_move} {tile_to_side(tile)} {tile.piece.type}') # reads off the location color and piece
        possible_moves = get_movement(tile) # gets where the piece on the given tile can move to
    
        if len(possible_moves) > 0:
            read("The piece on this tile can move to")
            read_off_list()

            return tile_to_move
        else:
            # if the possible moves array is empty the player cannot move
            read("There are no possible places for this piece to move to")
    
    return ""

# handles selecting where a piece can move to
def handle_moving_end(tile_to_move, tile_to_move_to):
    global possible_moves; global game_over

    starting_tile = get_tile_from_location(tile_to_move)
    ending_tile = get_tile_from_location(tile_to_move_to)

    # if the new tile is one of the possible moves
    if ending_tile in possible_moves:
        #Log code
        logRecord(f'{starting_tile.location} {starting_tile.piece.type} moving to {tile_to_move_to}')
        
        # confirm movement to player
        read(f'{starting_tile.location} {starting_tile.piece.type} moving to {tile_to_move_to}')
        promotion = move(starting_tile, ending_tile)  # move the piece on the tile to the new tile 

        
        
        if promotion == True:
            handle_promotion(ending_tile)
            
        # changes the turn
        if settings.turn == 'W':
            settings.turn = 'B'
        else:
            settings.turn = 'W'
        
        if is_in_check('W') is not False: # is_in_check will return a list if not false
            if is_in_check_mate('W'): # only check for checkmate if in check
                read("White in checkmate. The game is over. Black has won. Press 0 to restart the game.")
                game_over = True
            else: 
                read("White in check")
                logRecord("White in check")

        elif is_in_check('B') is not False: # is_in_check will return a list if not false
            if is_in_check_mate('B'): # only check for checkmate if in check
                read("Black in checkmate. The game is over. White has won. Press 0 to restart the game.")
                game_over = True
            else: 
                read("Black in check")
                logRecord("Black in check")
        
        if not game_over:
            read("It is now the other player's turn")
    else:
        read(f'{tile_to_move_to} is an illegal move')
    
    possible_moves = []
    
def handle_promotion(tile):
    displayBoard() # display whats on the board
    displayColumns() # show column letters
    displayRows() # show row numbers
    displayLog() # show log
    pygame.display.flip() #update the board
            
    text = "Press q for queen\nPress r for rook\nPress b for bishop\nPress k for knight"
    read(f'Your {tile.piece.type} can be promoted')
    lines = text.split("\n")
    
    #Code to handle log
    if tile.piece.side == "b":
        color = "black"
    else:
        color = "white"

    # the user can select while the possible options are being read
    for line in lines:
        for event in pygame.event.get():
             # if the user pressed a key
            if event.type == pygame.KEYDOWN:
                if event.key == 98:
                    promotion(tile, "Bishop")
                    logRecord(f"{color} {tile.piece.type} promoted to Bishop")
                    return True
                if event.key == 107:
                    promotion(tile, "Knight")
                    logRecord(f"{color} {tile.piece.type} promoted to Knight")
                    return True
                if event.key == 113:
                    promotion(tile, "Queen")
                    logRecord(f"{color} {tile.piece.type} promoted to Queen")
                    return True
                if event.key == 114:
                    promotion(tile, "Rook")
                    logRecord(f"{color} {tile.piece.type} promoted to Rook")
                    return True
        read(line)
    
    # for if the options have already been read
    while(True):
        for event in pygame.event.get():
             # if the user pressed a key
            if event.type == pygame.KEYDOWN:
                if event.key == 98:
                    promotion(tile, "Bishop")
                    logRecord(f"{color} {tile.piece.type} promoted to Bishop")
                    return True
                if event.key == 107:
                    promotion(tile, "Knight")
                    logRecord(f"{color} {tile.piece.type} promoted to Knight")
                    return True
                if event.key == 113:
                    promotion(tile, "Queen")
                    logRecord(f"{color} {tile.piece.type} promoted to Queen")
                    return True
                if event.key == 114:
                    promotion(tile, "Rook")
                    logRecord(f"{color} {tile.piece.type} promoted to Rook")
                    return True
    
def restart_game():
    global possible_moves; global viewing_row; global viewing_col
    
    possible_moves = []
    viewing_row = -1; viewing_col = -1
    
    settings.turn = 'W'
    settings.board = create_board() # reset board

def handle_presses(key_value, tile_to_move, tile_to_move_to):
    global voice_rate; global curLog; global logArray
    
    # if the game is over the controls will be limited
    if game_over:
        if key_value == 48:
            restart_game()
            tile_to_move = ""
            tile_to_move_to = ""
        elif key_value == pygame.K_SPACE:
            read_off_controls()

    # controls for if the game is ongoing
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

    #Log controls
    elif key_value == pygame.K_PAGEUP:
        # Player is selecting a log one log up (so one log back)
        handle_log("up")
    elif key_value == pygame.K_PAGEDOWN:
        # player is selecting a log one log down (so one log forward)
        handle_log("down")
    elif key_value == pygame.K_j:
        # player wants to know the current log
        read(f"Reading log {curLog}")
        #read(logArray[curLog])

    elif 97 <= int(key_value) <= 104 and (len(tile_to_move) == 0 or len(tile_to_move) == 2 and len(tile_to_move_to) == 0):
        if len(tile_to_move) == 0:
            tile_to_move = chr(key_value)
        elif len(tile_to_move_to) == 0:
            tile_to_move_to = chr(key_value)
    # if the pressed key is between 1-8 and a-h was selected before
    elif 49 <= int(key_value) <= 56 and (len(tile_to_move) == 1 or len(tile_to_move) == 2 and len(tile_to_move_to) == 1):
        if len(tile_to_move) == 1:
            tile_to_move += chr(key_value)
            tile_to_move = handle_moving_start(tile_to_move) # we have a chess location and will start the move process
        elif len(tile_to_move_to) == 1:
            tile_to_move_to += chr(key_value)
            handle_moving_end(tile_to_move, tile_to_move_to)
            tile_to_move = ""; tile_to_move_to = "" # reset tiles
    elif key_value == 48:
        restart_game()
        tile_to_move = ""
        tile_to_move_to = ""
    elif key_value == 47:
        all_moves(settings.turn)
    elif key_value == 109:
        read_board()
    elif key_value == pygame.K_SPACE:
            read_off_controls()
    elif key_value == 45:
        if voice_rate > -50:
            voice_rate -= 50
    elif key_value == 61:
        if voice_rate < 600:
            voice_rate += 50
    else: 
        print(key_value)
        tile_to_move = ""
        tile_to_move_to = ""
    
    return tile_to_move, tile_to_move_to

def start_display():
    global SCREEN; global FONT; global PIECE_FONT; 
    global viewing_row; global viewing_col;  global game_over; global opponent;
    global WINDOW_SIZE
    pygame.init() # initalizing pygame

    #Acquiring user monitor deets.
    USR_MONITOR = pygame.display.Info()
    USR_X = USR_MONITOR.current_w
    USR_Y = USR_MONITOR.current_h
    SCREEN_CENTER = (USR_X/2,USR_Y/2)
    WINDOW_SIZE = (USR_X,USR_Y)
    print(USR_X,USR_Y,SCREEN_CENTER)

    # determing size and fonts
    SCREEN = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    FONT = pygame.font.SysFont(None, 80)
    PIECE_FONT = pygame.font.Font("./assets/segoe-ui-symbol.ttf",80)
    
    tile_to_move = "" # for if the user is trying to select a tile
    tile_to_move_to = "" # for if the user is trying to select a tile to move to
    
    turn_one = True

    # a pygame loop that runs while the user is playing
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif opponent == "Comp":
                if settings.turn != settings.player_color:
                    engine_move = sieng.rand_move(settings.eng) # now let the engine make a move
                    
                    if engine_move == -1:
                        read("Black in checkmate. The game is over you have won. Press 0 to restart the game.")
                        game_over = True

            # if the user pressed a key
            elif event.type == pygame.KEYDOWN:
                tile_to_move, tile_to_move_to = handle_presses(event.key, tile_to_move, tile_to_move_to)

            displayBoard() # display whats on the board
            displayColumns() # show column letters
            displayRows() # show row numbers
            displayLog() # show log
            pygame.display.flip() #update the board
            
            if turn_one:
                read("Press C to play against the computer, Press V to play side-by-side with a friend")

                while(turn_one == True):
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == 99:
                                opponent == "Comp"
                                turn_one = False
                                
                            elif event.key == 118:
                                opponent == "Frnd"
                                turn_one = False
                    
                read("Press space to hear the keyboard controls")
                read("White starts")
                
if __name__ == "__main__":
    #Testing code exclusively for testing modules in the "game.py" file.
    #Please Remove code you are testing when you are finished.
    print("Test Begin")
    print(USR_MONITOR,USR_X,USR_Y)

    #Leave this print statement behind so that VScode doesn't freak for having an empty indent.
    print("Test End")