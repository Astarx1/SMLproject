from test.hex_board import hex_board_test_routine
from test.hex_ia import hex_IA_test_routine
from test.hex_game_manager import hex_game_manager_test_routine


try:
    print("Black win test running ...")
    hex_board_test_routine.test_win_black()
    print("Black win test OK !")
except Exception as e:
    print(e)

try:
    print("White win test running ...")
    hex_board_test_routine.test_win_white()
    print("White win test OK !")
except Exception as e:
    print(e)

try:
    print("IA test running ...")
    hex_IA_test_routine.run()
    print("IA test OK !")
except Exception as e:
    print(e)

try:
    print("Game manager test running ...")
    hex_game_manager_test_routine.run()
    print("IA test OK !")
except Exception as e:
    print(e)