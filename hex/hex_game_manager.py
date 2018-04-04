import random
from .hex_board import HexBoard

"""
In HexGameManager, we should separate the training and testing data !
"""

positions_letter = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7,
    'i': 8,
    'j': 9,
    'k': 10,
    'l': 11,
    'm': 12,
}


class HexGameManager:
    game_database = []
    file = ""

    def __init__(self, *args):
        pass

    def play_game(self, *args):
        pass

    @staticmethod
    def get_game(line=None, file="hex/data/raw_games.dat"):
        if HexGameManager.file is not file:
            with open(file, 'r') as f:
                content = f.readlines()
            content = [x.rstrip('\n') for x in content]

            player = 1
            for l in content:
                moves = l.split(' ')
                tmp = []
                for m in moves:
                    if len(m) is 2:
                        tmp.append((player, positions_letter[m[0]], int(m[1])))
                        player = -player
                HexGameManager.game_database.append(tmp)

            HexGameManager.file = file

        if line is None:
            line = random.randrange(len(HexGameManager.game_database))

        return HexGameManager.game_database[line]

    @staticmethod
    def get_random_move():
        good = False
        line = 0
        move = 0
        while not good:
            line = random.randrange(len(HexGameManager.game_database))
            move = random.randrange(2, len(HexGameManager.game_database[line]))-1
            if move > 0:
                good = True
        b = HexBoard()
        i = 0

        for m in HexGameManager.game_database[line]:
            b.play_move(m)
            i += 1
            if i >= move:
                break
        mat = b.get_copy_matrix()

        b = HexBoard()
        b.play_move(HexGameManager.game_database[line][move + 1])
        mat2 = b.get_copy_matrix()

        # Used to get the canonical board. I am not sure though
        # But we want the probabilities for the next player
        mat = HexGameManager.game_database[line][move + 1][0] * mat

        return mat, HexBoard.board_to_array(mat2), 1


