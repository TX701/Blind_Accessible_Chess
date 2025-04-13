import pygame, sys
import py.settings as settings
import pyttsx3
from py.chess import get_col_chess, get_tile_location, convert_to_location, move
from py.movement import move_manager

WHITE = (255,255,255)
BROWN = (180,135,100)
TAN = (240,216,181)
LIGHTGREEN = (67,93,73)
BLACK = (0,0,0)

def displayBoard(screen, font):
    pygame.draw.rect(screen,LIGHTGREEN,(0,0,1920,1080))
    pygame.draw.rect(screen,BLACK,(350,130,820,820), width = 10)
    
    for r in range(8):
        for c in range(8):
            if ((r % 2 == 0) and (c % 2 == 0)) or ((r %2 == 1) and (c%2 == 1)):
                square = pygame.draw.rect(screen, TAN, (360 + (r * 100), 140 + (c * 100), 100, 100))
            else:
                square = pygame.draw.rect(screen, BROWN, (360 + (r * 100), 140 + (c * 100), 100, 100))

            text = font.render(settings.board[c][r].piece.name, True, (0, 0, 0)) 
            rect = text.get_rect(center = (square.centerx, square.centery))
            screen.blit(text, rect)

def displayColumns(screen, font):
    width = 410
    for i in range(1, 9):
        row = font.render(get_col_chess(i - 1), True, BLACK)
        w,h = font.size(get_col_chess(i))
        
        screen.blit(row,(width-w,110-(h/2)))
        width += 100

def displayRows(screen, font):
    height = 190
    for i in range(1, 9):
        row = font.render(str(9-i), True, BLACK)
        w,h = font.size(str(9-i))
        screen.blit(row,(325-w,height-(h/2)))
        height += 100

def read(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def get_information(viewing_row, viewing_col):
    location = f'{chr(viewing_col + 65)}{viewing_row + 1}'
    type = settings.board[viewing_row][viewing_col].piece.type
    side = "Black" if settings.board[viewing_row][viewing_col].piece.side == "B" else "White"
    side_type = "nothing" if type == None else f'a {side} {type}'

    read(f'{location} contains {side_type}')

def handle_arrow_view(type, viewing_row, viewing_col):
    if viewing_row == -1 or viewing_col == -1:
        viewing_row = 0; viewing_col = 0
    elif (type == "U"):
        viewing_row = viewing_row - 1 if viewing_row != 0 else viewing_row
    elif (type == "R"):
        viewing_col = viewing_col + 1 if viewing_col != 7 else viewing_col
    elif (type == "D"):
        viewing_row = viewing_row + 1 if viewing_row != 7 else viewing_row
    elif (type == "L"):
        viewing_col = viewing_col - 1 if viewing_col != 0 else viewing_col
        
    get_information(viewing_row, viewing_col)
    return viewing_row, viewing_col

def handle_moving_start(current_tile):
    tile = get_tile_location(current_tile)
    side = "Black" if tile.piece.side == "B" else "White" if tile.piece.side == "W" else ""
    read(f'Selected {current_tile} {side} {tile.piece.type}')
    possible_moves = move_manager(tile)

    if tile.piece.type == None:
        read("There are no pieces on this tile")
    elif tile.piece.side != settings.turn:
        read("this piece cannot be moved this turn")
    elif len(possible_moves) > 0:
        read("The piece on this tile can move to")

        for i in possible_moves:
            if (i.piece.side != 'N'):
                side = "Black" if i.piece.side == "B" else "White"
                read(f'{i.location} {side} {i.piece.type}')
            else: read(i.location)

        handle_moving_end(tile, possible_moves)
    else:
        read("There are no possible places for this tile to move to")
    
    current_tile = ""

def handle_moving_end(tile_to_move, possible_moves):
    waiting = True

    current_tile = ""

    while(waiting):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key_value = event.key
                # if the pressed key is between a - h and the current_tile is 0
                if 97 <= int(key_value) <= 104 and len(current_tile) == 0:
                    current_tile = chr(key_value)
                elif 49 <= int(key_value) <= 56 and len(current_tile) == 1:
                    current_tile += chr(key_value)

                    if get_tile_location(current_tile) in possible_moves:
                        move(tile_to_move, get_tile_location(current_tile))

                        #changes the turn
                        if settings.turn == 'W':
                            settings.turn = 'B'
                        else:
                            settings.turn = 'W'

                        read(f'{tile_to_move.location} {get_tile_location(current_tile).piece.type} moving to {current_tile}')
                    else:
                        read(f'{current_tile} is an illegal move')

                    current_tile = ""
                    waiting = False

def start_display():
    engine = pyttsx3.init()

    pygame.init()

    window_size = (1920, 1000) 
    screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
    font = pygame.font.SysFont(None, 80)
    piece_font = pygame.font.Font("./assets/segoe-ui-symbol.ttf",80)
    
    current_tile = ""

    viewing_row = -1; viewing_col = -1

    while True:
        #A necessary line to prevent the whole thing from freezing lol.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



            if event.type == pygame.KEYDOWN:
                key_value = event.key
                # if the pressed key is between a - h and the current_tile is 0
                if 97 <= int(key_value) <= 104 and len(current_tile) == 0:
                    current_tile = chr(key_value)
                elif 49 <= int(key_value) <= 56 and len(current_tile) == 1:
                    current_tile += chr(key_value)
                    handle_moving_start(current_tile)
                    current_tile = ""
                elif event.key == pygame.K_UP:
                    viewing_row, viewing_col = handle_arrow_view("U", viewing_row, viewing_col)
                elif event.key == pygame.K_RIGHT:
                    viewing_row, viewing_col =  handle_arrow_view("R", viewing_row, viewing_col)
                elif event.key == pygame.K_DOWN:
                    viewing_row, viewing_col =  handle_arrow_view("D", viewing_row, viewing_col)
                elif event.key == pygame.K_LEFT:
                    viewing_row, viewing_col =  handle_arrow_view("L", viewing_row, viewing_col)
                else: 
                    current_tile = ""

        displayBoard(screen, piece_font)
        displayColumns(screen, font)
        displayRows(screen, font)
        pygame.display.flip() #update the board (this is used to reflect any changes made to the 2D array)

        engine.runAndWait()