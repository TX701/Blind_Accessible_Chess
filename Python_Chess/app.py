import settings
import pyttsx3
from chess import create_board, print_board
from movement import move_manager

def main():
    settings.init()
    settings.board = create_board()
    print_board()
    arr = move_manager(settings.board[1][0])
    
    for i in arr:
        print(i.location)

    engine = pyttsx3.init()
    engine.say("beep boop beep bop beep")
    engine.runAndWait()

if __name__ == "__main__":
    main()
