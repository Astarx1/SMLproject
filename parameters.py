class Params:
    BOARD_SIZE = 5
    BLACK = 1
    FIRST_PLAYER = 1
    WHITE = -1

    @staticmethod
    def get_next_player(player):
        return -player

    @staticmethod
    def prt(file, s):
        print("@" + file + " --- " + s)

    @staticmethod
    def log(file, s):
        Params.prt(file, s)
