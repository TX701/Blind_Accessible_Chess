import settings
from movement import move_manager

class Piece:
    def __init__(self, type, name, side):
        self.type = type
        self.name = name 
        self.side = side # remember colors look reversed in the terminal so black will look white. white is the one thats just outlines

class Tile:
    def __init__(self, col, row, location, piece):
        self.col = col
        self.row = row 
        self.location = location
        self.piece = piece

def get_col_chess(col):
    return chr(col + 65)

def convert_to_location(col, row):
    return get_col_chess(col) + str((8 - int(row)))

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
    if tile.piece.type != None: #if the tile (with the piece you want to move) has a piece
        end_tile.piece = tile.piece # for the tile youre moving to, change its piece to the given tiles piece
        tile.piece = Piece(None, " ", 'N') # for the given tile set its piece to an empty Piece
                
#checks if given side is in check (tested and should work)
def is_in_check(side):
    opposing_side = 'W' if (side == 'B') else 'B'
    tiles_with_pieces = get_pieces(opposing_side) # get all pieces from opposing side

    for tile_with_piece in tiles_with_pieces:
        opposing_possible_moves = move_manager(tile_with_piece)
        
        for element in opposing_possible_moves:
            if element.piece.type == "King": # if one of the pieces from the opposing team can move to the king, place in check (is this correct?)
                return True
    
    return False

# returns true if a check can be avoided false if not (only rudimentary tests)
def block_check(tile_with_piece):
    possible_moves = move_manager(tile_with_piece)
    
    for tile in possible_moves:
        original_tile = tile_with_piece
        original_possible_move_tile = tile
        
        move(tile_with_piece, tile)
        
        if not is_in_check(tile_with_piece.piece.side):
            return True
        
        move(tile_with_piece, original_tile)
        move(tile, original_possible_move_tile)
        
    return False

# takes in a side and returns true if that side is in checkmate false if that side has possible moves to get out of checkmate
def check_mate(side):
    tiles_with_pieces = get_pieces(side)

    for tile_with_piece in tiles_with_pieces:
        if (block_check(tile_with_piece) is True):
            return False
    
    return True   

tiles = []

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

    tiles.append(Tile(0, 7, "A1", Piece("Rook", "♖", 'W')))
    tiles.append(Tile(1, 7, "B1", Piece("Knight", "♘", 'W')))
    tiles.append(Tile(2, 7, "C1", Piece("Bishop", "♗", 'W')))
    tiles.append(Tile(3, 7, "D1", Piece("Queen", "♕", 'W')))
    tiles.append(Tile(4, 7, "E1", Piece("King", "♔", 'W')))
    tiles.append(Tile(5, 7, "F1", Piece("Bishop", "♗", 'W')))
    tiles.append(Tile(6, 7, "G1", Piece("Knight", "♘", 'W')))
    tiles.append(Tile(7, 7, "H1", Piece("Rook", "♖", 'W')))  
    
def get_tile(c, r):
    for tile in tiles:
        if(tile.col == c and tile.row == r):
            return tile
    return None

def get_tile_location(location):
    location = location.upper()

    for row in range(len(settings.board)):
        for col in range(len(settings.board[row])):
            if(settings.board[row][col].location == location):
                return settings.board[row][col]
    return None

def create_board():
    tile_set_up()

    board = []
    for r in range(8):
        row = []
        for c in range(8):
            tile = get_tile(c, r)
            if tile is not None:
                row.append(tile)
            else:
                row.append(Tile(c, r, convert_to_location(c, r), Piece(None, " ", 'N')))
        board.append(row)

    return board