import random

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

