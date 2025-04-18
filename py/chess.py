import py.settings as settings
from py.movement import move_manager, same_side

class Piece:
    def __init__(self, type, name, side):
        self.type = type
        self.name = name # will be a symbol that represents the piece
        self.side = side # 'B' or 'W'

class Tile:
    def __init__(self, col, row, location, piece):
        self.col = col
        self.row = row 
        self.location = location # A6 B8 etc
        self.piece = piece

def get_col_chess(col):
    return chr(col + 65) # converts 0 to A- 1 to B- 2 to C- etc

def convert_to_location(col, row):
    return get_col_chess(col) + str((8 - int(row))) # converts 0, 0 to A8

# gets all pieces from one side
def get_pieces(side):
    array_of_pieces = []
    for r in range(8):
        for c in range(8):
            if (settings.board[r][c].piece.side == side):
                array_of_pieces.append(settings.board[r][c])

    return array_of_pieces

# simple move function
def move(tile, end_tile):
    if tile.piece.type != None:  # if the tile (with the piece you want to move) has a piece
        if end_tile.piece.side != settings.turn:
            end_tile.piece = tile.piece  # for the tile youre moving to, change its piece to the given tiles piece
            tile.piece = Piece(None, " ", 'N')  # for the given tile set its piece to an empty Piece

# get a sides king piece
def get_king(side):
    tiles = get_pieces(side)

    for tile in tiles:
        if tile.piece.type == "King":
            return tile

# check if a side can capture a specific piece
def can_capture(capturing_side, tile_to_capture):
    capture_piece = []
    tiles_with_pieces = get_pieces(capturing_side) # get all pieces from the side that wants to capture 

    for tile_with_piece in tiles_with_pieces:
        opposing_possible_moves = move_manager(tile_with_piece)
        
        for element in opposing_possible_moves:
            if element == tile_to_capture and not same_side(element, tile_with_piece): # if one of the pieces from the opposing team can move to the king, place in check
                capture_piece.append(tile_with_piece)

    return capture_piece

def can_block(possible_check_tile, side_in_check):
    # move all pieces in side_in_check to all their possible possible moves
    # if one removes king from possible_check_tiles movement list- return true
    # if nothing can prevent the king from being captured- return false

    return ""
    
#checks if given side is in check
def is_in_check(side):
    opposing_side = 'W' if (side == 'B') else 'B'
    check_pieces = can_capture(opposing_side, get_king(side))

    if len(check_pieces) > 0:
        return check_pieces # if in check return a list of tiles that cause the check
    
    return False # if not in check return false

# takes in a side and returns true if that side is in checkmate false if that side has possible moves to get out of checkmate
def is_in_check_mate(side):
    check_pieces = is_in_check(side) # will be False if not in check- returns a list of tiles if in check

    if type(check_pieces) is list:
        if len(check_pieces) > 1:
            return True # if the list is bigger than 1, multiple pieces are attacking the king and the player cannot protect the king (fact check this)
        elif len(check_pieces) == 1:
            # if the list is a single element, check if that element can be caputured
            can_capture_check = can_capture(side, check_pieces[0])
            if len(can_capture_check) > 0:
                return False
            else: 
                if can_block:
                    return False
                else: return True
    
    return False

tiles = []

# initalizing our tiles and pieces
def tile_set_up():
    tiles.append(Tile(0, 0, "A8", Piece("Rook", "♜", 'B')))
    tiles.append(Tile(1, 0, "B8", Piece("Knight", "♞", 'B')))
    tiles.append(Tile(2, 0, "C8", Piece("Bishop", "♝", 'B')))
    tiles.append(Tile(3, 0, "D8", Piece("Queen", "♛", 'B')))
    tiles.append(Tile(4, 0, "E8", Piece("King", "♚", 'B')))
    tiles.append(Tile(5, 0, "F8", Piece("Bishop", "♝", 'B')))
    tiles.append(Tile(6, 0, "G8", Piece("Knight", "♞", 'B')))
    tiles.append(Tile(7, 0, "H8", Piece("Rook", "♜", 'B')))

    for i in range(8, 16):
        tiles.append(Tile(i - 8, 1, convert_to_location(i - 8, 1), Piece("Pawn", "♟", 'B')))
        tiles.append(Tile(i - 8, 6, convert_to_location(i - 8, 6), Piece("Pawn", "♙", 'W')))

    # tiles.append(Tile(3, 1, convert_to_location(3, 1), Piece("Pawn", "♙", 'W')))
    # tiles.append(Tile(4, 1, convert_to_location(4, 1), Piece("Pawn", "♙", 'W')))
    # tiles.append(Tile(5, 1, convert_to_location(5, 1), Piece("Pawn", "♙", 'W')))

    tiles.append(Tile(0, 7, "A1", Piece("Rook", "♖", 'W')))
    tiles.append(Tile(1, 7, "B1", Piece("Knight", "♘", 'W')))
    tiles.append(Tile(2, 7, "C1", Piece("Bishop", "♗", 'W')))
    tiles.append(Tile(3, 7, "D1", Piece("Queen", "♕", 'W')))
    tiles.append(Tile(4, 7, "E1", Piece("King", "♔", 'W')))
    tiles.append(Tile(5, 7, "F1", Piece("Bishop", "♗", 'W')))
    tiles.append(Tile(6, 7, "G1", Piece("Knight", "♘", 'W')))
    tiles.append(Tile(7, 7, "H1", Piece("Rook", "♖", 'W')))  
    
# given a row and col returns what piece should be there (used when building the board)
def get_tile(r, c):
    for tile in tiles:
        if(tile.col == c and tile.row == r):
            return tile
    return None

# gets the tile that is at a given location 
def get_tile_from_location(location):
    location = location.upper() # convert to upper case to accept a6 and A6

    for row in range(len(settings.board)):
        for col in range(len(settings.board[row])):
            if(settings.board[row][col].location == location):
                return settings.board[row][col]
    return None

def create_board():
    tile_set_up() # initalizing tiles

    board = []; 
    for r in range(8):
        row = []

        for c in range(8):
            tile = get_tile(r, c)
            if tile is not None:
                row.append(tile) # if there is supposed to be a tile at this given row col- add it
            else:
                row.append(Tile(c, r, convert_to_location(c, r), Piece(None, " ", 'N')))

        board.append(row)

    return board
