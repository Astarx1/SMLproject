import sys
sys.path.append("/home/romain/PycharmProjects/Hex/")

from hex.hex_game_manager import HexGameManager
from hex.hex_board import HexBoard
import traceback


class hex_game_manager_test_routine:
    @staticmethod
    def run():
        try:
            print("Game manager test running ...")
            hex_game_manager_test_routine.get_game()
            hex_game_manager_test_routine.get_move()
            print("Game manager test OK !")
        except Exception:
            traceback.print_exc()

    @staticmethod
    def get_game():
        game = HexGameManager.get_game(file="5by5self.dat", format="advanced")
        b = HexBoard()
        for g in game:
            b.play_move(g)
        b.find_if_winner(game[-1])
        print(b.winner())

    @staticmethod
    def get_move():
        game, p, v = HexGameManager.get_random_move(file="5by5self.dat", format="advanced")
        print(game)
        print(p)
        print(v)

hex_game_manager_test_routine.run()