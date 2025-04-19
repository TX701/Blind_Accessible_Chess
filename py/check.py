import py.settings as settings
from py.chess import Piece
from py.movement import move_manager, same_side

#checks if given side is in check
def is_in_check(side):
    opposing_side = 'W' if (side == 'B') else 'B'
    check_pieces = can_capture(opposing_side, get_king(side))

    if len(check_pieces) > 0:
        return check_pieces # if in check return a list of tiles that cause the check
    
    return False # if not in check return false

# gets all pieces from one side
def get_pieces(side):
    array_of_pieces = []
    for r in range(8):
        for c in range(8):
            if (settings.board[r][c].piece.side == side):
                array_of_pieces.append(settings.board[r][c])

    return array_of_pieces

# moves a piece and returns false if the side is still in check
def can_move_test(tile, end_tile):
    side = tile.piece.side
    tile_original_piece = tile.piece
    end_tile_original_piece = end_tile.piece
    
    end_tile.piece = tile_original_piece
    tile.piece = tile.piece = Piece(None, " ", 'N')
    
    in_check = type(is_in_check(side)) is list

    end_tile.piece = end_tile_original_piece
    tile.piece = tile_original_piece
    
    if in_check:
        return False # in_check is a list- so the piece is still in check moving did not help
        
    return True

def clean_list(tile, possible_moves):
    allowed_moves = []
    for move in possible_moves:
        if can_move_test(tile, move):
            allowed_moves.append(move)
            
    return allowed_moves

def all_possible_moves(side):
    tiles = get_pieces(side)
    
    possible_moves = []
    
    for tile in tiles:
        possible_moves.extend(get_movement(tile))
        
    return possible_moves

def get_movement(tile):
    possible_moves = move_manager(tile)
    
    if len(possible_moves) < 1:
        return []
    
    return clean_list(tile, possible_moves)

# simple move function
def move(tile, end_tile):
    if tile.piece.type != None:  # if the tile (with the piece you want to move) has a piece
        if end_tile.piece.side != settings.turn:
            end_tile.piece = tile.piece  # for the tile youre moving to, change its piece to the given tiles piece
            tile.piece = Piece(None, " ", 'N')  # for the given tile set its piece to an empty Piece
    
    # changes the turn
        if settings.turn == 'W':
            settings.turn = 'B'
        else:
            settings.turn = 'W'

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

# takes in a side and returns true if that side is in checkmate false if that side has possible moves to get out of checkmate
def is_in_check_mate(side):
    check_pieces = is_in_check(side) # will be False if not in check- returns a list of tiles if in check
    if type(check_pieces) is list:
        possible_moves = all_possible_moves(side)
        print(possible_moves)
        if len(possible_moves) < 1:
            return True
    
    return False