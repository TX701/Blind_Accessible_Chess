import settings

def get_type(tile):
    return tile.piece.type

def get_side(tile):
    return tile.piece.side

def same_side(tile1, tile2):
    tile1_side = get_side(tile1)
    tile2_side = get_side(tile2)
    if (tile1_side == tile2_side and tile1_side != 'N' and tile2_side != 'N'):
        return True
    return False

def tile_math(start, col_diff, row_diff):
    new_col = start.col + col_diff
    new_row = start.row + row_diff

    if (-1 < new_col < 8 and -1 < new_row < 8):
        return settings.board[new_row][new_col]
    
    return None

def move_manager(tile):
    type = get_type(tile)

    if (type == "Pawn"):
        return pawnMovement(tile)
    elif (type == "Rook"):
        return rookMovement(tile)
    elif (type == "Knight"):
        return knightMovement(tile)
    elif (type == "Bishop"):
        return bishopMovement(tile)
    elif (type == "Queen"):
        return queenMovement(tile)
    elif (type == "King"):
        return kingMovement(tile)
    
    return None

def get_line(starting_tile, col_inc, row_inc):
    line = []

    knight = False
    if (get_type(starting_tile) == "Knight"):
        knight =  True

    next_tile = tile_math(starting_tile, col_inc, row_inc)

    while (next_tile != None):
        if (get_type(next_tile) == None or knight):
            line.append(next_tile)
        elif (not same_side(starting_tile, next_tile)):
            line.append(next_tile)
            return line
        else:
            return line
    
    return line

def get_plus(tile_with_piece):
    lines = []

    get_line(tile_with_piece, 1, 0)
    get_line(tile_with_piece, -1, 0)
    get_line(tile_with_piece, 0, 1)
    get_line(tile_with_piece, 0, -1)

    return list(set(lines))

def get_cross(tile_with_piece):
    lines = []

    get_line(tile_with_piece, 1, 1)
    get_line(tile_with_piece, 1, -1)
    get_line(tile_with_piece, -1, 1)
    get_line(tile_with_piece, -1, -1)

    return list(set(lines))

def get_square(tile_with_piece, length):
    start = int(0 - (length/2))
    end = int(0 + (length/2) + 1)
    square = []

    for c in range(start, end):
        for r in range(start, end):
            tile = tile_math(tile_with_piece, c, r)
            if tile != None and tile != tile_with_piece:
                square.append(tile)

    return list(set(square))

def check_diagonal(tile, direction, row_movement, possible_moves):
    diagonal = tile_math(tile, direction, row_movement)
    if diagonal != None and get_type(diagonal) != None:
        possible_moves.append(diagonal)

def pawnMovement(tile_with_pawn):
    possible_moves = []
    row_movement = 1 if get_side(tile_with_pawn) == 'W' else -1

    check_diagonal(tile_with_pawn, -1, row_movement, possible_moves)
    check_diagonal(tile_with_pawn, 1, row_movement, possible_moves)

    forward = tile_math(tile_with_pawn, 0, row_movement)
    if forward != None and get_type(forward) == None:
        possible_moves.append(forward)

        forward_forward = tile_math(tile_with_pawn, 0, row_movement * 2)
        if forward_forward != None and get_type(forward_forward) == None:
            if ((get_side(tile_with_pawn) == 'W' and tile_with_pawn.row == 1) or (get_side(tile_with_pawn) == 'B' and tile_with_pawn.row == 6)):
                possible_moves.append(forward_forward)

    return possible_moves

def rookMovement(tile_with_rook):
    return get_plus(tile_with_rook)

def knightMovement(tile_with_knight):
    possible_moves = []
    unwanted = []

    possible_moves.append(get_square(tile_with_knight, 5))

    unwanted.append(get_square(tile_with_knight, 3))
    unwanted.append(get_plus(tile_with_knight))
    unwanted.append(get_cross(tile_with_knight))

    in_unwated = list(set(unwanted))

    return possible_moves - in_unwated

def bishopMovement(tile_with_bishop):
    return get_cross(tile_with_bishop)

def queenMovement(tile_with_queen):
    possible_moves = []

    possible_moves.append(get_plus(tile_with_queen))
    possible_moves.append(get_cross(tile_with_queen))

    return list(set(possible_moves))

def kingMovement(tile_with_king):
    return get_square(tile_with_king, 3)