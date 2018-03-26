from uct import UCT
from hex.hex_ia import HexIA
from hex.hex_board import HexBoard, WHITE


class hex_IA_test_routine:
    @staticmethod
    def run():
        ia = HexIA()
        board = HexBoard()
        u = UCT(ia)
        u.next_turn(board, WHITE)

