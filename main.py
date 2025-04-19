from py.game import start_display
import py.settings as settings
from py.chess import create_board, is_in_check, is_in_check_mate
import py.engine as engine

if __name__ == "__main__":
    settings.init() # creating the board global variable
    settings.board = create_board() # creating the board with the inital piece

    start_display() # starting the display and game loop