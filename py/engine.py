import py.chess as ch
import random as rand
import py.movement as movement
import py.settings as settings
import py.game as game
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


def rand_move(e):
    #pick random tiles until it contains a piece with the correct color

    while(True):
        row = chr(rand.randint(97, 104))
        col = chr(rand.randint(49, 56))
        rand_tile = ch.get_tile_from_location(row + col)

        if rand_tile.piece != None:
            if rand_tile.piece.side == settings.eng.side:
                all_moves = movement.move_manager(rand_tile)
                if len(all_moves) > 0:
                    target_tile = rand.choice(all_moves)
                    text = "opponent is moving the "+ rand_tile.piece.type + " on "+ rand_tile.location+ "to "+ target_tile.location
                    game.read(text)
                    ch.move(rand_tile, target_tile)
                    break
    if ch.is_in_check(settings.player_color):
        game.read("You are in check!")


