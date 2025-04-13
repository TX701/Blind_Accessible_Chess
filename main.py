from py.game import start_display
import py.settings as settings
from py.chess import create_board
import py.engine as engine

def main():
    settings.init() # creating the board global variable
    settings.board = create_board() # creating the board with the inital piece
    
    start_display() # starting the display and game loop
    
if __name__ == "__main__":
    main()
