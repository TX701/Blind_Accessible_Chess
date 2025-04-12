import pygame, sys, settings
from chess import get_col_chess, create_board

def displayBoard(screen, font):
    pygame.draw.rect(screen,LIGHTGREEN,(0,0,1920,1080))
    pygame.draw.rect(screen,BLACK,(350,130,820,820), width = 10)
    
    for r in range(8):
        for c in range(8):
            if ((r % 2 == 0) and (c % 2 == 0)) or ((r %2 == 1) and (c%2 == 1)):
                square = pygame.draw.rect(screen,TAN,(360+(r*100),140+(c*100),100,100))
            else:
                square = pygame.draw.rect(screen,BROWN,(360+(r*100),140+(c*100),100,100))

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
        row = font.render(str(i), True, BLACK)
        w,h = font.size(str(i))
        screen.blit(row,(325-w,height-(h/2)))
        height += 100

WHITE = (255,255,255)
BROWN = (180,135,100)
TAN = (240,216,181)
LIGHTGREEN = (67,93,73)
BLACK = (0,0,0)

def get_key_press():
    keys = pygame.key.get_pressed()

    for i in keys:
        if i != False:
            return i
        
    return False

def start_display():
    pygame.init()

    window_size = (100, 1080) 
    screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
    font = pygame.font.SysFont(None, 80)
    piece_font = pygame.font.Font("segoe-ui-symbol.ttf",80)
    
    current_tile = ""

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
                else: current_tile = ""

        displayBoard(screen, piece_font)
        displayColumns(screen, font)
        displayRows(screen, font)
        #Display.flip() updates the display to actually show what we've "drawn" onto the screen. Time delay is so that the loop doesn't grow too large too fast, perhaps not necessary.
        pygame.display.flip()
        
        if len(current_tile) == 2:
            print(current_tile)
            current_tile = ""
        else: pygame.time.delay(1000)