import pygame
import sys
#from chess import 

#The purpose of this file is to hold methods related to User Input and Graphical User Interface.


#This method will create an 8x8 grid of black brown and white pieces.
def displayBoard(screen):
    #Drawing the background
    pygame.draw.rect(screen,LIGHTGREEN,(0,0,1920,1080))
    
    #Drawing Board Border
    pygame.draw.rect(screen,BLACK,(350,130,820,820), width = 10)
    
    #Drawing Board Tiles
    for r in range(8):
        for c in range(8):
            #If the row is even (starting with zeroth row) and the column is even (starting at zeroth column) then that tile will "white", else black.
            #But if the row is odd, and the column is also odd, then that tile will also be "white" (This should work.)
            if ((r % 2 == 0) and (c % 2 == 0)) or ((r %2 == 1) and (c%2 == 1)):
                pygame.draw.rect(screen,TAN,(360+(r*100),140+(c*100),100,100))
            else:
                pygame.draw.rect(screen,BROWN,(360+(r*100),140+(c*100),100,100))

def displayColumns(screen):
    #This isn't the best way to do this. I'm just lazy.
    col = font.render("A", True, BLACK)
    w,h = font.size("A")
    screen.blit(col,(410-(w/2),110 - h,100,100))
    col = font.render("B", True, BLACK)
    w,h = font.size("B")
    screen.blit(col,(510-(w/2),110 - h,100,100))
    col = font.render("C", True, BLACK)
    w,h = font.size("C")
    screen.blit(col,(610-(w/2),110 - h,100,100))
    col = font.render("D", True, BLACK)
    w,h = font.size("D")
    screen.blit(col,(710-(w/2),110 - h,100,100))
    col = font.render("E", True, BLACK)
    w,h = font.size("E")
    screen.blit(col,(810-(w/2),110 - h,100,100))
    col = font.render("F", True, BLACK)
    w,h = font.size("F")
    screen.blit(col,(910-(w/2),110 - h,100,100))
    col = font.render("G", True, BLACK)
    w,h = font.size("G")
    screen.blit(col,(1010-(w/2),110 - h,100,100))
    col = font.render("H", True, BLACK)
    w,h = font.size("H")
    screen.blit(col,(1110-(w/2),110 - h,100,100))

def displayRows(screen):
    #Same as above.
    row = font.render("1", True, BLACK)
    w,h = font.size("1")
    screen.blit(row,(325-w,190-(h/2)))
    row = font.render("2", True, BLACK)
    w,h = font.size("2")
    screen.blit(row,(325-w,290-(h/2)))
    row = font.render("3", True, BLACK)
    w,h = font.size("3")
    screen.blit(row,(325-w,390-(h/2)))
    row = font.render("4", True, BLACK)
    w,h = font.size("4")
    screen.blit(row,(325-w,490-(h/2)))
    row = font.render("5", True, BLACK)
    w,h = font.size("5")
    screen.blit(row,(325-w,590-(h/2)))
    row = font.render("6", True, BLACK)
    w,h = font.size("6")
    screen.blit(row,(325-w,690-(h/2)))
    row = font.render("7", True, BLACK)
    w,h = font.size("7")
    screen.blit(row,(325-w,790-(h/2)))
    row = font.render("8", True, BLACK)
    w,h = font.size("8")
    screen.blit(row,(325-w,890-(h/2)))



#def displayPieces(screen):


#Testing code for the game methods. Much of this will also be initialized in the main method. It is copied here for testing purposes.
if __name__ == "__main__":
    #Initializes the pygame library.
    pygame.init()
    
    #Initilizes our pygame font object.
    font = pygame.font.SysFont(None, 80)

    #Set's a window size (My (sam's) monitor is 1920 by 1080 so it's set to that.) and then creates a screen object using that size.
    #The screen is basically the in code representation of the user's monitor screen.
    #We will be displaying things on the screen by "painting" them onto this screen object.
    window_size = (1920, 1080) 
    screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

    #Initializing colors to use.
    WHITE = (255,255,255)
    BROWN = (180,135,100)
    TAN = (240,216,181)
    LIGHTGREEN = (67,93,73)
    BLACK = (0,0,0)

    #Testing Methods
    while True:
        #A necessary line to prevent the whole thing from freezing lol.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                

        #Function call to displayBoard
        displayBoard(screen)
        displayColumns(screen)
        displayRows(screen)
        #Display.flip() updates the display to actually show what we've "drawn" onto the screen. Time delay is so that the loop doesn't grow too large too fast, perhaps not necessary.
        pygame.display.flip()
        pygame.time.delay(1000)