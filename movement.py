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

def get_line(start, col_inc, row_inc):
    line = []

    knight = get_side(start) is not None and get_type(start) == "Knight"

    new_tile = tile_math(start, col_inc, row_inc)
    while new_tile is not None:
        if get_type(new_tile) is None:
            line.append(new_tile)
            new_tile = tile_math(new_tile, col_inc, row_inc)
        elif not same_side(new_tile, start):
            line.append(new_tile)

            if (knight):
                new_tile = tile_math(new_tile, col_inc, row_inc)
            else:
                return line
        else:
            return line

    return line

def get_plus(tile_with_piece):
    lines = []

    lines.extend(get_line(tile_with_piece, 1, 0))
    lines.extend(get_line(tile_with_piece, -1, 0))
    lines.extend(get_line(tile_with_piece, 0, 1))
    lines.extend(get_line(tile_with_piece, 0, -1))

    return lines

def get_cross(tile_with_piece):
    lines = []

    lines.extend(get_line(tile_with_piece, 1, 1))
    lines.extend(get_line(tile_with_piece, 1, -1))
    lines.extend(get_line(tile_with_piece, -1, 1))
    lines.extend(get_line(tile_with_piece, -1, -1))

    return lines

def get_square(tile_with_piece, length):
    start = int(0 - (length/2))
    end = int(0 + (length/2) + 1)
    square = []
    
    for r in range(start, end):
        for c in range(start, end):
            tile = tile_math(tile_with_piece, c, r)
            
            if tile != None and tile != tile_with_piece:
                square.append(tile)
                
    return square

def check_diagonal(tile, direction, row_movement, possible_moves):
    diagonal = tile_math(tile, direction, row_movement)
    if diagonal != None and get_type(diagonal) != None:
        possible_moves.append(diagonal)

def pawnMovement(tile_with_pawn):
    possible_moves = []
    row_movement = -1 if get_side(tile_with_pawn) == 'W' else 1

    check_diagonal(tile_with_pawn, -1, row_movement, possible_moves)
    check_diagonal(tile_with_pawn, 1, row_movement, possible_moves)

    forward = tile_math(tile_with_pawn, 0, row_movement)
    if forward != None and get_type(forward) == None:
        possible_moves.append(forward)

        forward_forward = tile_math(tile_with_pawn, 0, row_movement * 2)
        if forward_forward != None and get_type(forward_forward) == None:
            if ((get_side(tile_with_pawn) == 'W' and tile_with_pawn.row == 6) or (get_side(tile_with_pawn) == 'B' and tile_with_pawn.row == 1)):
                possible_moves.append(forward_forward)

    return possible_moves

def rookMovement(tile_with_rook):
    return get_plus(tile_with_rook)

def knightMovement(tile_with_knight):
    possible_moves = []
    unwanted = []

    possible_moves.extend(get_square(tile_with_knight, 5))

    # unwanted.extend(get_square(tile_with_knight, 3))
    unwanted.extend(get_plus(tile_with_knight))
    unwanted.extend(get_cross(tile_with_knight))
    
    # return None
    return [x for x in possible_moves if x not in unwanted]

def bishopMovement(tile_with_bishop):
    return get_cross(tile_with_bishop)

def queenMovement(tile_with_queen):
    possible_moves = []

    possible_moves.extend(get_plus(tile_with_queen))
    possible_moves.extend(get_cross(tile_with_queen))

    return possible_moves

def kingMovement(tile_with_king):
    return get_square(tile_with_king, 3)