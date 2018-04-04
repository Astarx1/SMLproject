from hex.hex_board import HexBoard, WHITE, BLACK
import traceback


class hex_board_test_routine:
    @staticmethod
    def run():
        try:
            hex_board_test_routine.test_win_black()
            print("Black win test OK !")
        except Exception as e:
            traceback.print_exc()
            print(e)
        try:
            hex_board_test_routine.test_win_white()
            print("White win test OK !")
        except Exception as e:
            traceback.print_exc()
            print(e)
        try:
            hex_board_test_routine.test_win_mixed()
            print("Mixed win test OK !")
        except Exception as e:
            traceback.print_exc()
            print(e)

    @staticmethod
    def test_win_black():
        b = HexBoard()

        b.play_move((BLACK,0,0))
        b.play_move((BLACK,0,1))
        b.play_move((BLACK,0,2))
        b.play_move((BLACK,0,3))
        b.play_move((BLACK,0,4))
        b.play_move((BLACK,0,5))
        b.play_move((BLACK,0,6))
        b.play_move((BLACK,0,7))
        b.play_move((BLACK,0,8))
        b.play_move((BLACK,0,9))
        b.play_move((BLACK,0,10))
        b.play_move((BLACK,0,11))
        b.play_move((BLACK,0,12))
        b.find_if_winner((BLACK, 0, 12))
        assert(b.winner() == BLACK)
        
        b = HexBoard()

        b.play_move((BLACK,0,0))
        b.play_move((BLACK,0,1))
        b.play_move((BLACK,0,2))
        b.play_move((BLACK,0,3))
        b.play_move((BLACK,0,4))
        b.play_move((BLACK,1,4))
        b.play_move((BLACK,1,5))
        b.play_move((BLACK,1,6))
        b.play_move((BLACK,1,7))
        b.play_move((BLACK,1,8))
        b.play_move((BLACK,0,8))
        b.play_move((BLACK,0,9))
        b.play_move((BLACK,0,10))
        b.play_move((BLACK,0,11))
        b.play_move((BLACK,0,12))
        b.find_if_winner((BLACK, 0, 12))
        assert(b.winner() == BLACK)

        b = HexBoard()
        b.play_move((BLACK,7,0))
        b.play_move((BLACK,7,1))
        b.play_move((BLACK,7,2))
        b.play_move((BLACK,7,3))
        b.play_move((BLACK,7,4))
        b.play_move((BLACK,7,5))
        b.play_move((BLACK,8,6))
        b.play_move((BLACK,7,7))
        b.play_move((BLACK,6,8))
        b.play_move((BLACK,10,9))
        b.play_move((BLACK,11,10))
        b.play_move((BLACK,12,11))
        b.play_move((BLACK,12,12))
        b.find_if_winner((BLACK, 0, 12))
        assert(b.winner() is not BLACK)

    @staticmethod
    def test_win_white():
        b = HexBoard()

        b.play_move((WHITE, 0, 0))
        b.play_move((WHITE, 1, 0))
        b.play_move((WHITE, 2, 0))
        b.play_move((WHITE, 3, 0))
        b.play_move((WHITE, 4, 0))
        b.play_move((WHITE, 5, 0))
        b.play_move((WHITE, 6, 0))
        b.play_move((WHITE, 7, 0))
        b.play_move((WHITE, 8, 0))
        b.play_move((WHITE, 9, 0))
        b.play_move((WHITE, 10, 0))
        b.play_move((WHITE, 11, 0))
        b.play_move((WHITE, 12, 0))
        b.find_if_winner((WHITE, 12, 0))
        assert (b.winner() == WHITE)

        b = HexBoard()

        b.play_move((WHITE, 0, 0))
        b.play_move((WHITE, 1, 0))
        b.play_move((WHITE, 2, 0))
        b.play_move((WHITE, 3, 0))
        b.play_move((WHITE, 4, 0))
        b.play_move((WHITE, 4, 1))
        b.play_move((WHITE, 5, 1))
        b.play_move((WHITE, 6, 1))
        b.play_move((WHITE, 7, 1))
        b.play_move((WHITE, 8, 1))
        b.play_move((WHITE, 8, 0))
        b.play_move((WHITE, 9, 0))
        b.play_move((WHITE, 10, 0))
        b.play_move((WHITE, 11, 0))
        b.play_move((WHITE, 12, 0))
        b.find_if_winner((WHITE, 12, 0))

        assert (b.winner() == WHITE)

        b = HexBoard()

        b.play_move((WHITE, 0, 10))
        b.play_move((WHITE, 1, 0))
        b.play_move((WHITE, 2, 0))
        b.play_move((WHITE, 3, 0))
        b.play_move((WHITE, 4, 0))
        b.play_move((WHITE, 4, 1))
        b.play_move((WHITE, 5, 1))
        b.play_move((WHITE, 6, 1))
        b.play_move((WHITE, 7, 1))
        b.play_move((WHITE, 8, 1))
        b.play_move((WHITE, 8, 0))
        b.play_move((WHITE, 9, 0))
        b.play_move((WHITE, 10, 0))
        b.play_move((WHITE, 11, 0))
        b.play_move((WHITE, 12, 0))
        b.find_if_winner((WHITE, 12, 0))

        assert (b.winner() is not WHITE)

    @staticmethod
    def test_win_mixed():
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
        b.play_move((WHITE, 9, 0))
        b.play_move((WHITE, 10, 0))
        b.play_move((WHITE, 11, 0))
        b.play_move((WHITE, 12, 0))
        b.find_if_winner((WHITE, 12, 0))

        assert (b.winner() is WHITE)

