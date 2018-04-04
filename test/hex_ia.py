from uct import UCT
from hex.hex_ia import HexIARandom, HexIA, args
from hex.hex_game_manager import HexGameManager
from hex.hex_board import HexBoard, WHITE
import traceback


class hex_IA_test_routine:
    @staticmethod
    def run():
        try:
            print("IA Random test running ...")
            hex_IA_test_routine.test_UCT_with_random()
            hex_IA_test_routine.test_NN_training()
            print("IA Random test OK !")


        except Exception:
            traceback.print_exc()

    @staticmethod
    def test_UCT_with_random():
        ia = HexIARandom()
        board = HexBoard()
        u = UCT(ia)
        u.next_turn(board, WHITE)

    @staticmethod
    def test_NN_training():
        nn = HexIA()
        gm = HexGameManager

        moves = []
        while len(moves) < args['batch_size']:
            b, v, p = gm.get_random_move()
            moves.append((b, v, p))

        nn.train(moves)

