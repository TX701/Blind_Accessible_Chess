import settings
from chess import create_board, print_board
from movement import move_manager

def main():
    settings.init()
    settings.board = create_board()
    print_board()
    arr = move_manager(settings.board[1][0])
    
    for i in arr:
        print(i.location)

if __name__ == "__main__":
    main()
