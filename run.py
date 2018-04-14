from test.hex_board import hex_board_test_routine
from test.hex_ia import hex_IA_test_routine
from test.hex_game_manager import hex_game_manager_test_routine
from test.hex_coach import hex_coach_test_routine
from parameters import Params
import tensorflow as tf
import keras.backend.tensorflow_backend as K

# hex_board_test_routine.run()
# hex_game_manager_test_routine.run()
# hex_IA_test_routine.run()

if Params.CUDA:
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    K.set_session(sess)

hex_coach_test_routine.run()
