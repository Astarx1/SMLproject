import sys


class Params:
    BOARD_SIZE = 5
    BLACK = 1
    FIRST_PLAYER = 1
    WHITE = -1

    # Games Save
    STANDARD_GAME_FILE = "hex/data/5by5self.dat"
    STANDARD_FORMAT = "advanced"

    # Neural Network Parameters
    NUMBER_FILTERS = 32
    CUDA = False
    BATCH_SIZE = 64
    EPOCS = 20

    # Coach Parameters
    TAKE_FROM_CHECKPOINT = True
    NN_CHECKPOINT_FOLDER = "checkpoint"
    NN_CHECKPOINT_FILENAME = "checkpoint.pth.tar"
    RESET_GAMES_AFTER_BATCH = 10
    NUMBER_GAMES_BATCH = 5
    
    @staticmethod
    def get_next_player(player):
        return -player

    forbidden_files = [
        "hex_game_manager.py"
    ]
    @staticmethod
    def prt(file, s):
        if file in Params.forbidden_files:
            return
        print("@" + file + " --- " + s)

    @staticmethod
    def log(file, s):
        Params.prt(file, s)

    @staticmethod
    def ongoing():
        sys.stdout.write('.')
        sys.stdout.flush()

    @staticmethod
    def end_ongoing():
        print("")

