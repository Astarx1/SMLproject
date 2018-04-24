import sys


class Params:
    BOARD_SIZE = 7
    BLACK = 1
    FIRST_PLAYER = 1
    WHITE = -1
    NOT_PLAYED = 0

    # UCT
    GAUSSIAN_SIGMA = 0.03
    RANDOM_FACTOR_CONSTANT = 0
    EXPLORATION_BONUS = 0.1
    METHOD_STOP = "time"
    VALUE_STOP = 4.0
    COMPUTE_WIN = False  # Not implemented !

    # Games Save
    STANDARD_GAME_FILE = "hex/data/7by7self.dat"
    STANDARD_FORMAT = "advanced"

    # Neural Network Parameters
    NUMBER_FILTERS_CN_1 = 49
    NUMBER_FILTERS_CN_2 = 49
    NUMBER_FILTERS_CN_3 = 25
    NUMBER_FILTERS_CN_4 = 25
    CUDA = False
    BATCH_SIZE = 60
    EPOCS = 7

    # Coach Parameters
    TAKE_FROM_CHECKPOINT = True
    GAME_SET_METHOD = "maximum"
    RESET_GAMES_AFTER_BATCH = 1  # If GAME_SET_METHOD = "reset"
    MAXIMUM_GAMES_BATCH = 4  # Id GAME_SET_METHOD = "maximum"
    NUMBER_GAMES_BATCH = 1  # When the training is run
    SAVING_FROM_CONVERGENCE_TO_ERROR = 3
    RII_PARAMETER = 0.99
    INFOS_MAX_SIZE = 1000  # To avoid overflow
    SAVE_INFOS = 10
    INFOS_FILE = "hex/data/infos7v7.dat"

    # Checkpoint storage
    NN_CHECKPOINT_FOLDER = "checkpoint"

    STORE_AFTER = 75  # Put at -1 in order to never create specific checkpoints
    PREFIX_NAME = "check"
    UTC_VERSION = "v1"
    NEURAL_VERSION = "v2"
    BOARD_VERSION = "b7x7v2"
    SEPARATOR = "_"
    SUFFIX = ".pth.tar"
    WORKING_CHECKPOINT_FILENAME = "working_checkpoint" + SUFFIX

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


