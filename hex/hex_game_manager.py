import random
from .hex_board import HexBoard, BOARD_SIZE, BLACK
import traceback

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
    0: 'a',
    1: 'b',
    2: 'c',
    3: 'd',
    4: 'e',
    5: 'f',
    6: 'g',
    7: 'h',
    8: 'i',
    9: 'j',
    10: 'k',
    11: 'l',
    12: 'm',
    13: 'n',
}


class UnknownFormat(Exception):
    pass


class BadFormat(Exception):
    pass


class HexGameManager:
    game_database = {}

    def __init__(self, *args):
        pass

    def play_game(self, *args):
        pass

    @staticmethod
    def write_format_advanced(moves, args, file):
        with open(file, "a") as mf:
            a = args["player1"] + "," + args["player2"] + "," + str(moves[0][0]*args["winner"]) + ":"
            ms = []
            for m in moves:
                ms.append(positions_letter[m[1]] + positions_letter[m[2]])
            a += ",".join(ms) + '\n'
            mf.write(a)

    @staticmethod
    def read_format_advanced(file):
        with open(file, 'r') as f:
            content = f.readlines()
        content = [x.rstrip('\n') for x in content]

        db = []
        for g in content:
            try:
                player = BLACK
                sep = g.split(":")
                tmp = {}
                infos = sep[0].split(",")
                moves = sep[1].split(",")

                tmp["infos"] = {"player1": infos[0], "player2": infos[1], "winner": int(infos[2])}
                tmp["moves"] = []

                for m in moves:
                    tmp["moves"].append((player, positions_letter[m[0]], positions_letter[m[1]]))
                    player = -player
                db.append(tmp)
            except Exception:
                traceback.print_exc()
                raise BadFormat

        return db

    @staticmethod
    def read_format_raw_pos(file):
        with open(file, 'r') as f:
            content = f.readlines()
        content = [x.rstrip('\n') for x in content]

        db = []
        for l in content:
            player = 1
            moves = l.split(' ')
            tmp = []
            for m in moves:
                if len(m) is 2:
                    if 0 < int(m[1]) < BOARD_SIZE:
                        tmp.append((player, positions_letter[m[0]], int(m[1])))
                elif len(m) is 3:
                    if 0 < int(m[1] + m[2]) < BOARD_SIZE:
                        tmp.append((player, positions_letter[m[0]], int(m[1] + m[2])))
                elif len(m) is 0:
                    continue
                else:
                    raise BadFormat

                player = -player
            db.append({"moves": tmp})
        return db

    @staticmethod
    def update_file(file, format="raw_pos"):
        HexGameManager.game_database[file] = []

        d = []
        if format is "advanced":
            d = HexGameManager.read_format_advanced(file)
        elif format is "raw_pos":
            d = HexGameManager.read_format_raw_pos(file)
        else:
            raise UnknownFormat

        for g in d:
            HexGameManager.game_database[file].append(g)

    @staticmethod
    def get_game(line=None, file="hex/data/raw_games.dat", format="raw_pos"):
        if file not in HexGameManager.game_database:
            HexGameManager.game_database[file] = []

            d = []
            if format is "advanced":
                d = HexGameManager.read_format_advanced(file)
            elif format is "raw_pos":
                d = HexGameManager.read_format_raw_pos(file)
            else:
                raise UnknownFormat

            for g in d:
                HexGameManager.game_database[file].append(g)

        if line is None:
            line = random.randrange(len(HexGameManager.game_database))

        return HexGameManager.game_database[file][line]["moves"]

    @staticmethod
    def get_random_move():
        good = False
        file = random.choice(list(HexGameManager.game_database.keys()))
        line = 0
        move = 0
        while not good:
            line = random.randrange(len(HexGameManager.game_database[file]))
            move = random.randrange(2, len(HexGameManager.game_database[file][line]["moves"]))-1
            if move > 0:
                good = True
        b = HexBoard()
        i = 0

        for m in HexGameManager.game_database[file][line]["moves"]:
            b.play_move(m)
            i += 1
            if i >= move:
                break
        mat = b.get_copy_matrix()

        b = HexBoard()
        b.play_move(HexGameManager.game_database[file][line]["moves"][move + 1])
        mat2 = b.get_copy_matrix()

        # Used to get the canonical board. I am not sure though
        # But we want the probabilities for the next player
        mat = HexGameManager.game_database[file][line]["moves"][move + 1][0] * mat

        return mat, HexBoard.board_to_array(mat2), 1


