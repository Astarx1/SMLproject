from uct import UCT
from hex.hex_ia import HexIARandom, HexIA, args
from hex.hex_game_manager import HexGameManager
from hex.hex_board import HexBoard, WHITE, BLACK
import traceback


class hex_IA_test_routine:
    @staticmethod
    def run():
        try:
            print("IA CNN test running ...")
            hex_IA_test_routine.test_UCT_with_random()
            hex_IA_test_routine.test_NN_training()
            hex_IA_test_routine.test_NN_predict()
            print("IA CNN test OK !")


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

    @staticmethod
    def test_NN_predict():
        nn = HexIA(load_checkpoint=True)

        b = HexBoard()

        b.play_move((WHITE, 0, 0))
        b.play_move((WHITE, 1, 0))
        b.play_move((WHITE, 2, 0))
        b.play_move((WHITE, 3, 0))
        b.play_move((WHITE, 4, 0))
        b.play_move((WHITE, 4, 1))
        b.play_move((WHITE, 5, 1))
        b.play_move((WHITE, 6, 1))
        b.play_move((BLACK, 6, 2))
        b.play_move((WHITE, 7, 1))
        b.play_move((WHITE, 8, 1))
        b.play_move((WHITE, 8, 0))
        b.play_move((WHITE, 11, 0))
        b.play_move((WHITE, 12, 0))

        mat = b.get_copy_matrix()

        r = nn.get_proba(mat)
        print(str(r))