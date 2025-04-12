from game import start_display, read
import settings
from chess import create_board

def main():
    settings.init()
    settings.board = create_board()
    
    start_display()
    
if __name__ == "__main__":
    main()