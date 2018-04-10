import time
import datetime
from math import sqrt, log
from parameters import Params
import random


class Node:
    UCTK = Params.EXPLORATION_BONUS

    def __init__(self, board, ia, move, father, color, interestingness):
        self.board = board
        self.ia = ia

        self.father = father
        self.children = []
        self.color = -color

        self.move = None
        if move is not None:
            self.move = move

        self.val_exploit = interestingness
        self.p = None
        self.proba = None
        self.expansions = 1

        self.update_proba()

    def add_child(self, move, father, value):
        nc = Node(self.board, self.ia, move, father, self.color, value)
        self.children.append(nc)

    def select_child_expand(self):
        s = sorted(self.children,
                   key=lambda c: c.proba - c.val_exploit*Node.UCTK*sqrt(2*log(self.expansions)/c.expansions)
                   )[0]
        return s

    def get_best_child_move(self):
        s = sorted(self.children,
                   key=lambda c: c.proba + Params.RANDOM_FACTOR_CONSTANT*random.gauss(0, Params.GAUSSIAN_SIGMA)
                   )[0]
        return s.move, self.expansions

    def expand_node(self):
        if len(self.children) == 0:
            moves = self.get_moves_list()
            nb = self.board.get_legal_moves_play_list(moves)

            c = self.color
            if self.move is not None:
                c = -self.move[0]

            for m in nb:
                self.add_child((c, m[0], m[1]), self, self.p[self.board.board_size*m[0]+m[1]])

            self.update_proba()
        else:
            self.select_child_expand().expand_node()
            self.update_proba()
            self.update_expansion()

    def get_moves_list(self):
        if self.father is not None:
            return [self.move] + self.father.get_moves_list()
        else:
            return []

    def compute_ia_proba(self):
        moves = self.get_moves_list()
        # We multiply by self.move[0][0] to get the "canonical board"
        c = self.color
        if self.move is not None:
            c = self.move[0]
        self.p, self.proba = self.ia.get_proba(c*self.board.get_matrix_play_list(moves))

    def update_proba(self):
        if len(self.children) == 0:
            self.compute_ia_proba()
        else:
            for c in self.children:
                self.min_max(c.proba)

    def min_max(self, proba):
        if self.move is None:
            return
        if (1-proba) > self.proba:
            self.proba = 1-proba

    def update_expansion(self):
        self.expansions = 0
        for c in self.children:
            self.expansions += c.expansions

    def __str__(self):
        t = []
        for c in self.children:
            t.append({"move": c.move, "interest": c.val_exploit, "proba": c.proba})
        return str(t)

class UCT:
    def __init__(self, ia, *args, **kwargs):
        self.ia = ia
        self.root = None

        seconds = kwargs.get('time', 1.0)
        self.calculation_time = seconds

    def next_turn(self, board, color, args={"method": Params.METHOD_STOP, "value": Params.VALUE_STOP}):
        self.root = Node(board, self.ia, None, None, -color, 0)
        value_init = self.get_init_value(args)
        value = value_init
        rollouts = 0
        while self.check_continue(value, value_init, args):
            self.root.expand_node()
            value = self.update_value(value, args)
            rollouts += 1
        bm, exp = self.root.get_best_child_move()
        return bm, exp, rollouts

    def get_init_value(self, args):
        if args["method"] == "time":
            return time.time()
        elif args["method"] == "rollouts":
            return 0

    def check_continue(self, value, value_init, args):
        if value - value_init < args["value"]:
            return True
        return False

    def update_value(self, value, args):
        if args["method"] == "time":
            return time.time()
        elif args["method"] == "rollouts":
            return value + 1
