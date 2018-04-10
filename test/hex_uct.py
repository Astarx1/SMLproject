import sys
sys.path.append("/home/romain/PycharmProjects/Hex/")

from uct import UCT
from hex.hex_ia import HexAIFake
from hex.hex_board import HexBoard, WHITE, BLACK
import traceback


class hex_IA_test_routine:
    @staticmethod
    def run():
        try:
            print("UCT test running ...")
            hex_IA_test_routine.test_UCT_with_fake()
            print("UCT test OK !")

        except Exception:
            traceback.print_exc()

    @staticmethod
    def test_UCT_with_fake():
        ia = HexAIFake()
        board = HexBoard()
        u = UCT(ia)
        m = u.next_turn(board, BLACK)[0]

        print(m)
        print(u.root)

        assert(m is (1, 0, 0))

        board.play_move(m)

hex_IA_test_routine.run()