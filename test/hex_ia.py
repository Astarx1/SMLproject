from uct import UCT
from hex.hex_ia import HexIARandom
from hex.hex_board import HexBoard, WHITE


class hex_IA_test_routine:
    @staticmethod
    def run():
        ia = HexIARandom()
        board = HexBoard()
        u = UCT(ia)
        u.next_turn(board, WHITE)

