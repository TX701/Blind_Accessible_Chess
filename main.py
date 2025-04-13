from py.game import start_display, read
import py.settings as settings
from py.chess import create_board
import py.engine as engine

def main():
    settings.init()
    settings.board = create_board()

    start_display()
    
if __name__ == "__main__":
    main()