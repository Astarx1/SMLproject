import random
from .hex_board import HexBoard, BOARD_SIZE, BLACK
import traceback
from parameters import Params

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
class EmptyDB(Exception):
    pass


class HexGameManager:
    game_database = {}

    def __init__(self, *args):
        pass

    def play_game(self, *args):
        pass

    @staticmethod
    def write_add_format_advanced(moves, args, file=Params.STANDARD_GAME_FILE):
        """
        Advanced format should contain informations like the board used, the model of the NN, the setup and time for
        the UTC...
        Current format : [player1],[player2],[winner]:[",".join([moves])]
        """
        Params.prt("hex_game_manager.py", "Moves : " + str(moves))
        Params.prt("hex_game_manager.py", "Args : " + str(args))

        with open(file, "a") as mf:
            a = args["player1"] + "," + args["player2"] + "," + str(args["winner"]) + ":"
            ms = []
            for m in moves:
                ms.append(positions_letter[m[1]] + positions_letter[m[2]])
            a += ",".join(ms) + '\n'
            mf.write(a)

        if Params.GAME_SET_METHOD == "maximum":
            lines = []
            with open(file, "r") as mf:
                lines = mf.readlines()

            if len(lines) > Params.MAXIMUM_GAMES_BATCH:
                    lines.pop(0)

            with open(file, "w") as mf:
                for l in lines:
                    mf.write(l)

    @staticmethod
    def read_format_advanced(file=Params.STANDARD_GAME_FILE):
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
    def read_format_raw_pos(file=Params.STANDARD_GAME_FILE):
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
            db.append({"moves": tmp, "infos": {"winner": 1}})
        return db

    @staticmethod
    def update_file(file=Params.STANDARD_GAME_FILE, format=Params.STANDARD_FORMAT):
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
    def get_game(line=None, file=Params.STANDARD_GAME_FILE, format=Params.STANDARD_FORMAT):
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
    def get_random_move(file=Params.STANDARD_GAME_FILE, format=Params.STANDARD_FORMAT):
        good = False
        if file is None:
            if len(list(HexGameManager.game_database.keys())) > 0:
                file = random.choice(list(HexGameManager.game_database.keys()))
            else:
                raise EmptyDB

        HexGameManager.update_file(file, format)

        line = 0
        move = 0
        while not good:
            line = random.randrange(len(HexGameManager.game_database[file]))
            move = random.randrange(2, len(HexGameManager.game_database[file][line]["moves"]))-1
            if move > 0:
                good = True
        b = HexBoard()

        i = 0
        while i <= move:
            b.play_move(HexGameManager.game_database[file][line]["moves"][i])
            i += 1

        mat = b.get_copy_matrix()

        b = HexBoard()
        b.play_move(HexGameManager.game_database[file][line]["moves"][move + 1])

        # Used to get the canonical board. I am not sure though
        # But we want the probabilities for the next player
        mat2 = HexGameManager.game_database[file][line]["moves"][move+1][0] * b.get_copy_matrix()
        mat = HexGameManager.game_database[file][line]["moves"][move][0] * mat

        v = 0
        if (HexGameManager.game_database[file][line]["infos"]["winner"] is
            HexGameManager.game_database[file][line]["moves"][move + 1][0]):
            v = 1

        infos = {
            "winner": HexGameManager.game_database[file][line]["infos"]["winner"],
            "nb_moves": len(HexGameManager.game_database[file][line]["moves"])
        }

        Params.prt("hex_game_manager.py", "-------------")
        Params.prt("hex_game_manager.py", str(HexGameManager.game_database[file][line]["infos"]["winner"]))
        Params.prt("hex_game_manager.py", "Moves")
        Params.prt("hex_game_manager.py", str(HexGameManager.game_database[file][line]["moves"][move]))
        Params.prt("hex_game_manager.py", str(HexGameManager.game_database[file][line]["moves"][move + 1]))
        Params.prt("hex_game_manager.py", "Original :")
        Params.prt("hex_game_manager.py", str(HexGameManager.game_database[file][line]["moves"][move][0] * mat))
        Params.prt("hex_game_manager.py", HexGameManager.game_database[file][line]["moves"][move+1][0] * b.get_copy_matrix())
        Params.prt("hex_game_manager.py", "Altered")
        Params.prt("hex_game_manager.py", mat)
        Params.prt("hex_game_manager.py", mat2)
        Params.prt("hex_game_manager.py", "Infos transmitted")
        Params.prt("hex_game_manager.py", v)
        Params.prt("hex_game_manager.py", infos)
        Params.prt("hex_game_manager.py", "-------------")
        return mat, HexBoard.board_to_array(mat2), v, infos


