def init():
    global board # creates a global variable board
    global turn
    global player_color
    player_color = 'W' #make this variable later on but for now player is always white
    turn = 'W' #keeps track of the current colors turn, true if white false if black
    board = []