from .hex_ia import HexIA, dotdict, args
from .hex_board import HexBoard, WHITE, BLACK
from .hex_game_manager import HexGameManager

from uct import UCT
from parameters import Params

import time
import traceback


class ConvNetUnableToProduceGame(Exception):
    pass


class HexCoach:
    average_number_moves = []
    average_winner = []

    def __init__(self):
        self.last_checkpoint = "checkpoint.pth.tar"
        self.file_to_save = "games0"
        self.ai = HexIA()
        self.uct = UCT(self.ai)

        self.training_calls = 0

    def add_batch_file(self):
        player = Params.FIRST_PLAYER

        i = 0
        error_count = 0
        while i < Params.NUMBER_GAMES_BATCH:
            try:
                b = HexBoard()
                moves = []
                w = 0
                j = 0
                expansions = []
                rollouts = []
                ended = []

                start = time.time()
                while w == 0:
                    m, infos = self.uct.next_turn(b, player)
                    expansions.append(infos["expansions"])
                    rollouts.append(infos["rollouts"])
                    ended.append(infos["ended"])
                    player = Params.get_next_player(player)
                    moves.append(m)
                    b.play_move(m)
                    b.find_if_winner(m)
                    w = b.winner()
                    j += 1
                    Params.ongoing()
                end = time.time()

                Params.end_ongoing()
                Params.log("hex_coach.py", "Match : " + str(i + 1) + "/" + str(Params.NUMBER_GAMES_BATCH) +
                           " - " + str(end - start) + " sec")
                Params.log("hex_coach.py", "Winner : " + str(w))
                Params.log("hex_coach.py", "Moves (" + str(len(moves)) + ") : " + str(moves))
                Params.log("hex_coach.py", "Expansions : " + str(expansions))
                Params.log("hex_coach.py", "Rollouts : " + str(rollouts))
                Params.log("hex_coach.py", "Ended : " + str(ended))
                Params.log("hex_coach.py", "Matrix : \n" + str(b.get_copy_matrix()))
                args = {"player1": "cnn", "player2": "cnn", "winner": str(w)}
                HexGameManager.write_add_format_advanced(moves, args, "hex/data/5by5self.dat")
                i += 1
            except Exception:
                traceback.print_exc()
                time.sleep(0.1)
                Params.log("hex_coach.py", "Failure when creating game")

                error_count += 1
                if error_count >= Params.SAVING_FROM_CONVERGENCE_TO_ERROR:
                    raise ConvNetUnableToProduceGame

    def trainAI(self, checkpoint=Params.TAKE_FROM_CHECKPOINT):
        j = 0
        if checkpoint:
            try:
                infos = self.get_last_valid_checkpoint_name()
                if infos is not None:
                    self.ai.load_checkpoint(filename=infos["full"])
                    self.training_calls = infos["iters"]
                Params.prt("hex_coach.py", "Checkpoint Loaded : " + infos["full"])

            except:
                Params.log("hex_coach.py", "Unable to open the checkpoint")

        while True:
            try:
                if Params.GAME_SET_METHOD is "reset":
                    if j % Params.RESET_GAMES_AFTER_BATCH is 0:
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
                           str(HexCoach.average_number_moves[-1]) + ", number of learning iter : " +
                           str(self.training_calls) + ")")
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
        self.training_calls += 1
        if Params.STORE_AFTER > 0:
            if self.training_calls % Params.STORE_AFTER > 0:
               self.ai.save_checkpoint(filename=Params.WORKING_CHECKPOINT_FILENAME)
            else:
                name = self.give_checkpoint_name()
                self.ai.save_checkpoint(filename=name)
        else:
            self.ai.save_checkpoint(filename=Params.WORKING_CHECKPOINT_FILENAME)


    def give_checkpoint_name(self):
        name = Params.PREFIX_NAME
        utc_version = Params.UTC_VERSION
        neural_version = Params.NEURAL_VERSION
        board_version = Params.BOARD_VERSION
        sep = Params.SEPARATOR
        suffix = Params.SUFFIX

        iteration = str(self.training_calls)

        return name + sep + board_version + sep + utc_version + sep + neural_version + sep + iteration + suffix

    def get_checkpoint_informations(self, name):
        wp = name.split(".")[0]
        s = wp.split(Params.SEPARATOR)
        info = {"valid": False, "name": None, "board": None, "utc": None, "neural": None, "iters": None, "full": name}

        if len(s) is 5:
            try:
                info["name"] = s[0]
                info["board"] = s[1]
                info["utc"] = s[2]
                info["neural"] = s[3]
                info["iters"] = int(s[4])
                info["valid"] = True
            except:
                pass

        return info

    def get_last_valid_checkpoint_name(self, folder=Params.NN_CHECKPOINT_FOLDER):
        from os import walk
        f = []
        for (dirpath, dirnames, filenames) in walk(folder):
            f.extend(filenames)
            break
        p = []
        for v in f:
            ci = self.get_checkpoint_informations(v)
            if ci["valid"] is True:
                p.append(ci)
        if len(p) > 0:
            return sorted(p, key=lambda x: x["iters"], reverse=True)[0]
        else:
            return None


