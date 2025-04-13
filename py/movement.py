import py.settings as settings # needed to access global variable

def get_type(tile):
    return tile.piece.type # function to get the type of a piece

def get_side(tile):
    return tile.piece.side # function to get the type of side 

# checks if two pieces are from the same side (both black / both white)
def same_side(tile1, tile2):
    tile1_side = get_side(tile1) # side of first tile
    tile2_side = get_side(tile2) # side of second tile

    # if the two sides are not equal and both sides contain pieces
    if (tile1_side == tile2_side and tile1_side != 'N' and tile2_side != 'N'):
        return True
    
    return False

# from the perspective of a tile moves to another tile -1 for col moves up the board -1 for row moves to the left
def tile_math(start, col_diff, row_diff):
    new_col = start.col + col_diff # gets the new column index 
    new_row = start.row + row_diff # gets the new row index

    # if the col and row are between 0-7 (7 inclusive) then they fit on the chess board and can be returned
    if (-1 < new_col < 8 and -1 < new_row < 8):
        return settings.board[new_row][new_col]
    
    return None # the col and row will lead to some out of bounds error

# returns what moves a piece (which is on a tile) can make and splits off into different methods depending on what type the piece is
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

# from the perspective of a piece makes a vector using a col or row increment which will be 0, -1, or 1
def get_line(start, col_inc, row_inc):
    line = []

    # due to the knight mechanics we want to ignore collisions to be able to "jump" over pieces
    knight = get_side(start) is not None and get_type(start) == "Knight" 
    new_tile = tile_math(start, col_inc, row_inc) # gets a tile that is one unit away from the starting tile

    # if the new_tile exists on the board
    while new_tile is not None:
        # if the new tile has nothing on it or if the tile we are moving is a knight
        if get_type(new_tile) is None or knight:
            line.append(new_tile) # add new tile to the array
            new_tile = tile_math(new_tile, col_inc, row_inc) # get another new tile

        # if the new tile has  something on it but its not the same side as the piece we are moving
        elif not same_side(new_tile, start):
            line.append(new_tile) # add new tile to the vector
            return line # stop the function
        else:
            return line # stop the function

    return line # return the vector

# runs get line four times with specific configurations to get a plus shape
def get_plus(tile_with_piece):
    lines = []

    lines.extend(get_line(tile_with_piece, 1, 0)) # get a vector going down
    lines.extend(get_line(tile_with_piece, -1, 0)) # get a vector going up
    lines.extend(get_line(tile_with_piece, 0, 1)) # get a vector going right
    lines.extend(get_line(tile_with_piece, 0, -1)) # get a vector going left

    return lines # extend is used to merge the vectors together

# runs get line four times with specific configurations to get a cross shape
def get_cross(tile_with_piece):
    lines = []

    lines.extend(get_line(tile_with_piece, 1, 1)) # get a vector going down right
    lines.extend(get_line(tile_with_piece, 1, -1)) # get a vector going down left
    lines.extend(get_line(tile_with_piece, -1, 1)) # get a vector going up right
    lines.extend(get_line(tile_with_piece, -1, -1)) # get a vector going up left

    return lines # extend is used to merge the vectors together

# returns all tiles surrounding a specific tile, takes in a length to determine how big the square is
def get_square(tile_with_piece, length):
    start = int(0 - (length/2)) # starting increment is 0 - tile/2 
    end = int(0 + (length/2) + 1) # ending increment is 0 + tile/2
    square = []
    
    for r in range(start, end):
        for c in range(start, end):
            tile = tile_math(tile_with_piece, c, r) # gets a tile that is an incremenet away from the center tile
            
            # if the tile exists and is not equal to the center tile
            if tile != None and tile != tile_with_piece:
                square.append(tile) # add it to the square array
                
    return square

#  gets a tile that is diagonal to the given tile 
#  direction -1 goes to the left direction +1 goes to the right
#  row_movement goes up the board +1 row_movement goes down the board
def check_diagonal(tile, direction, row_movement, possible_moves):
    diagonal = tile_math(tile, direction, row_movement)
    # if the diagonal is a real piece and if the tile has something on it
    if diagonal != None and get_type(diagonal) != None and not same_side(diagonal, tile):
        possible_moves.append(diagonal) # append to the given array
        # we append rather than return since we need to make sure we dont append something that is null

def pawnMovement(tile_with_pawn):
    possible_moves = []
    row_movement = -1 if get_side(tile_with_pawn) == 'W' else 1 # determining if we are moving up or down the board

    # check sides
    check_diagonal(tile_with_pawn, -1, row_movement, possible_moves) # adds left diagonal to the array if its meets criteria 
    check_diagonal(tile_with_pawn, 1, row_movement, possible_moves) # adds right diagonal to the array if its meets criteria 

    forward = tile_math(tile_with_pawn, 0, row_movement)
    # if one forward exists and has no pieces
    if forward != None and get_type(forward) == None:
        possible_moves.append(forward) # add the the array

        forward_forward = tile_math(tile_with_pawn, 0, row_movement * 2)
        if get_type(forward_forward) == None:
            if ((get_side(tile_with_pawn) == 'W' and tile_with_pawn.row == 6) or (get_side(tile_with_pawn) == 'B' and tile_with_pawn.row == 1)):
                possible_moves.append(forward_forward)
                # if the pawn is on the correct row and if we added the forward tile add the next forward tile

    return possible_moves

def rookMovement(tile_with_rook):
    return get_plus(tile_with_rook)

def knightMovement(tile_with_knight):
    possible_moves = []
    unwanted = []

    possible_moves.extend(get_square(tile_with_knight, 5)) # gets a 5x5 square
 
    unwanted.extend(get_square(tile_with_knight, 3)) # gets a 3x3 square
    unwanted.extend(get_plus(tile_with_knight)) # gets a plus
    unwanted.extend(get_cross(tile_with_knight)) # gets a cross
    
    arr = [x for x in possible_moves if x not in unwanted] # removes all pieces that are in unwanted that are in possible_moves
    
    #remove any tiles in arr that contain pieces from the sames side as the knight
    for i in arr:
        if i.piece.side == tile_with_knight.piece.side:
            arr.remove(i)

    return arr

def bishopMovement(tile_with_bishop):
    return get_cross(tile_with_bishop)

def queenMovement(tile_with_queen):
    possible_moves = []

    possible_moves = possible_moves + get_plus(tile_with_queen) # gets a cross
    possible_moves.extend(get_cross(tile_with_queen)) # gets a plus

    return possible_moves

def kingMovement(tile_with_king):
    return get_square(tile_with_king, 3)
