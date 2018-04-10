from .hex_ia import HexIA, dotdict, args
from .hex_board import HexBoard, WHITE, BLACK
from .hex_game_manager import HexGameManager

from uct import UCT
from parameters import Params

import traceback


class HexCoach:
    average_number_moves = []
    average_winner = []

    def __init__(self):
        self.last_checkpoint = "checkpoint.pth.tar"
        self.file_to_save = "games0"
        self.ai = HexIA()
        self.uct = UCT(self.ai)

    def add_batch_file(self):
        player = Params.FIRST_PLAYER

        for i in range(Params.NUMBER_GAMES_BATCH):
            b = HexBoard()
            moves = []
            w = 0
            j = 0
            expansions = []
            rollouts = []

            while w == 0:
                m, r, ro = self.uct.next_turn(b, player)
                expansions.append(r)
                rollouts.append(ro)
                player = Params.get_next_player(player)
                moves.append(m)
                b.play_move(m)
                b.find_if_winner(m)
                w = b.winner()
                j += 1
                Params.ongoing()

            Params.end_ongoing()
            Params.log("hex_coach.py", "Match : " + str(i + 1) + "/" + str(Params.NUMBER_GAMES_BATCH))
            Params.log("hex_coach.py", "Winner : " + str(w))
            Params.log("hex_coach.py", "Moves (" + str(len(moves)) + ") : " + str(moves))
            Params.log("hex_coach.py", "Expansions : " + str(expansions))
            Params.log("hex_coach.py", "Rollouts : " + str(rollouts))
            Params.log("hex_coach.py", "Matrix : \n" + str(b.get_copy_matrix()))
            args = {"player1": "cnn", "player2": "cnn", "winner": str(w)}
            HexGameManager.write_add_format_advanced(moves, args, "hex/data/5by5self.dat")

    def trainAI(self, checkpoint=Params.TAKE_FROM_CHECKPOINT):
        j = 0
        if checkpoint:
            try:
                self.ai.load_checkpoint()
                Params.prt("hex_coach.py", "Checkpoint Loaded !")
            except:
                Params.log("hex_coach.py", "Unable to open the checkpoint")

        while True:
            try:
                if j % Params.RESET_GAMES_AFTER_BATCH is 0:
                    self.ai.save_checkpoint()
                    Params.prt("hex_coach.py", "Checkpoint saved")

                    import os
                    if os.path.isfile("hex/data/5by5self.dat"):
                        os.remove("hex/data/5by5self.dat")
                    Params.prt("hex_coach.py", "Games removed")

            except Exception:
                traceback.print_exc()
                Params.log("hex_coach.py", "Impossible to remove previous games")

            try:
                self.add_batch_file()
            except Exception:
                traceback.print_exc()
                Params.log("hex_coach.py", "Impossible to add Files")

            try:
                self.launch_train()
            except Exception:
                traceback.print_exc()
                Params.log("hex_coach.py", "Impossible to train the neural network")

            j += 1

            try:
                Params.log("hex_coach.py", "Round " + str(j + 1) + " (round " + str(j % Params.RESET_GAMES_AFTER_BATCH + 1)
                           + "/" + str(Params.RESET_GAMES_AFTER_BATCH) + ", average winner : " +
                           str(HexCoach.average_winner[-1]) + ", number of moves : " +
                           str(HexCoach.average_number_moves[-1]) + ")")
            except:
                traceback.print_exc()
                Params.log("hex_coach.py", "Impossible to view round work")

    def launch_train(self):
        gm = HexGameManager

        moves = []
        nb_moves = []
        winner = []
        while len(moves) < args['batch_size']:
            b, v, p, i = gm.get_random_move()
            moves.append((b, v, p))
            nb_moves.append(i["nb_moves"])
            winner.append(i["winner"])

        HexCoach.average_number_moves.append(0.0)
        for i in nb_moves:
            HexCoach.average_number_moves[-1] += i/len(nb_moves)
        HexCoach.average_winner.append(0.0)
        for i in winner:
            HexCoach.average_winner[-1] += i/len(winner)

        self.ai.train(moves)
        self.ai.save_checkpoint()
