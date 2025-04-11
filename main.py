import settings
from chess import create_board, print_board, is_in_check, check_mate, get_pieces, block_check
from movement import move_manager, same_side

def main():
    settings.init()
    settings.board = create_board()
    print_board()

    print(is_in_check('W'))
    
if __name__ == "__main__":
    main()
