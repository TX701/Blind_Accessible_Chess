import py.chess as ch

class engine:
    def __init__(self, side):
        self.side = side

# def engine_move(e):
#     if(ch.is_in_check(e.side)):
#         #check if there is a way out of mate if not you lose
#         #get out of mate by any means necessary
#         #if there are multiple ways to escape take the first one found
#         if(ch.block_check())
#
#     #does any random move



def all_possible_moves(e):
    all_pieces = ch.get_pieces(e.side)
    return all_pieces
    # all_moves = []
    # print(all_pieces)

    # for piece in all_pieces:
    #     all_moves +=

