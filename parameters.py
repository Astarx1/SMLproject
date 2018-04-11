import sys


class Params:
    BOARD_SIZE = 9
    BLACK = 1
    FIRST_PLAYER = 1
    WHITE = -1
    NOT_PLAYED = 0

    # UCT
    GAUSSIAN_SIGMA = 0.03
    RANDOM_FACTOR_CONSTANT = 0
    EXPLORATION_BONUS = 1
    METHOD_STOP = "time"
    VALUE_STOP = 1.0
    COMPUTE_WIN = False  # Not implemented !

    # Games Save
    STANDARD_GAME_FILE = "hex/data/5by5self.dat"
    STANDARD_FORMAT = "advanced"

    # Neural Network Parameters
    NUMBER_FILTERS_CN_1 = 128
    NUMBER_FILTERS_CN_2 = 64
    NUMBER_FILTERS_CN_3 = 32
    NUMBER_FILTERS_CN_4 = 16
    CUDA = False
    BATCH_SIZE = 60
    EPOCS = 20

    # Coach Parameters
    TAKE_FROM_CHECKPOINT = True
    NN_CHECKPOINT_FILENAME = "checkpoint.pth.tar"
    GAME_SET_METHOD = "maximum"
    RESET_GAMES_AFTER_BATCH = 1  # If GAME_SET_METHOD = "reset"
    MAXIMUM_GAMES_BATCH = 4  # Id GAME_SET_METHOD = "maximum"
    NUMBER_GAMES_BATCH = 1  # When the training is run
    SAVING_FROM_CONVERGENCE_TO_ERROR = 3

    # Checkpoint storage
    NN_CHECKPOINT_FOLDER = "checkpoint"

    STORE_AFTER = 500
    PREFIX_NAME = "check"
    UTC_VERSION = "v1"
    NEURAL_VERSION = "v1"
    BOARD_VERSION = "b5x5v1"
    SEPARATOR = "_"
    SUFFIX = ".pth.tar"

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
        print("@" + str(file) + " --- " + str(s))

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


