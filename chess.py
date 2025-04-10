import settings
from movement import move_manager

class Piece:
    def __init__(self, type, name, side):
        self.type = type
        self.name = name 
        self.side = side

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

def get_pieces(side, current_board):
    array_of_pieces = []
    for r in range(8):
        row = []
        for c in range(8):
            if (current_board[r][c].piece.side == side):
                array_of_pieces.append(current_board[r][c])
                
#checks if given side is in checkmate
def check(side, current_board):
    pieces = get_pieces(side)
    
    for piece in pieces:
        possible_moves = move_manager(piece)

        for move in possible_moves:
            if move.piece.type == "King":
                return True
    
    return False

tiles = []

def tile_set_up():
    tiles.append(Tile(0, 0, "A8", Piece("Rook", "♜", 'W')))
    tiles.append(Tile(1, 0, "B8", Piece("Knight", "♞", 'W')))
    tiles.append(Tile(2, 0, "C8", Piece("Bishop", "♝", 'W')))
    tiles.append(Tile(3, 0, "D8", Piece("Queen", "♛", 'W')))
    tiles.append(Tile(4, 0, "A6", Piece("King", "♚", 'W')))
    tiles.append(Tile(5, 0, "F8", Piece("Bishop", "♝", 'W')))
    tiles.append(Tile(6, 0, "G8", Piece("Knight", "♞", 'W')))
    tiles.append(Tile(7, 0, "H8", Piece("Rook", "♜", 'W')))

    for i in range(8, 16):
        tiles.append(Tile(i - 8, 1, convert_to_location(i - 8, 1), Piece("Pawn", "♟", 'W')))
        tiles.append(Tile(i - 8, 6, convert_to_location(i - 8, 6), Piece("Pawn", "♙", 'B')))

    tiles.append(Tile(0, 7, "A1", Piece("Rook", "♖", 'B')))
    tiles.append(Tile(1, 7, "B1", Piece("Knight", "♘", 'B')))
    tiles.append(Tile(2, 7, "C1", Piece("Bishop", "♗", 'B')))
    tiles.append(Tile(3, 7, "D1", Piece("Queen", "♕", 'B')))
    tiles.append(Tile(4, 7, "E1", Piece("King", "♔", 'B')))
    tiles.append(Tile(5, 7, "F1", Piece("Bishop", "♗", 'B')))
    tiles.append(Tile(6, 7, "G1", Piece("Knight", "♘", 'B')))
    tiles.append(Tile(7, 7, "H1", Piece("Rook", "♖", 'B')))  
    
def get_tile(c, r):
    for tile in tiles:
        if(tile.col == c and tile.row == r):
            return tile
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

def print_board():
    for r in range(len(settings.board)):
        print("\n")
        for c in range(len(settings.board[r])):
            print(settings.board[r][c].piece.name, end="")
    print("\n")