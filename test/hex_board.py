from hex.hex_board import HexBoard, WHITE, BLACK


class hex_board_test_routine:
    @staticmethod
    def test_win():
        b = HexBoard()

        b.play_move((BLACK,0,0))
        b.play_move((BLACK,0,1))
        b.play_move((BLACK,0,2))
        b.play_move((BLACK,0,3))
        b.play_move((BLACK,1,4))
        b.play_move((BLACK,0,5))
        b.play_move((BLACK,0,6))
        b.play_move((BLACK,0,7))
        b.play_move((BLACK,0,8))
        b.play_move((BLACK,0,9))
        b.play_move((BLACK,0,10))

        print(b.get_repr_matrix())

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
        b.play_move((BLACK,10,10))
        assert(b.winner() == BLACK)

