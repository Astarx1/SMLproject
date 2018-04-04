from hex.hex_game_manager import HexGameManager
from hex.hex_board import HexBoard
import traceback


class hex_game_manager_test_routine:
    @staticmethod
    def run():
        try:
            game = HexGameManager.get_game()
            b = HexBoard()
            for g in game:
                b.play_move(g)
            b.find_if_winner(game[-1])
            print(b)
            print(b.winner())
        except Exception as e:
            traceback.print_exc()
