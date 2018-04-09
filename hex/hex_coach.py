from .hex_ia import HexIA, dotdict
from .hex_board import HexBoard, WHITE, BLACK
from .hex_game_manager import HexGameManager

from uct import UCT
from parameters import Params

import time

session_args = dotdict({
    "matches_batch": 1,
    "format": "advanced"
})


class HexCoach:
    def __init__(self):
        self.last_checkpoint = "checkpoint.pth.tar"
        self.file_to_save = "games0"
        self.ai = HexIA()
        self.uct = UCT(self.ai)

    def add_batch_file(self):
        player = Params.FIRST_PLAYER

        for i in range(session_args["matches_batch"]):
            b = HexBoard()
            moves = []
            w = 0
            j = 0
            while w == 0:
                Params.log("hex_coach.py", "Move " + str(j) + ", game " + str(i) + "/" +
                           str(session_args["matches_batch"]))
                j += 1
                m = self.uct.next_turn(b, player)
                player = Params.get_next_player(player)
                moves.append(m)
                b.play_move(m)
                b.find_if_winner(m)
                w = b.winner()
            Params.prt("hex_coach.py", "Winner : " + str(w))
            Params.prt("hex_coach.py", "Moves : " + str(moves))
            Params.prt("hex_coach.py", "Matrix : \n" + str(b.get_copy_matrix()))
            args = {"player1": "cnn", "player2": "cnn", "winner": str(w)}
            HexGameManager.write_add_format_advanced(moves, args, "hex/data/5by5self.dat")

    def trainAI(self):
        pass
