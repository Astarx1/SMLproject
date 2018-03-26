import time
import datetime
from math import sqrt, log


class Node:
    UCTK = 0.0001

    def __init__(self, board, ia, move, father, color):
        self.board = board
        self.ia = ia

        self.father = father
        self.children = []
        self.color = color

        self.move = None
        if move is not None:
            self.move = move
        else:
            self.move = (-color, 0, 0)

        self.proba = None
        self.expansions = 1

        self.update_proba()

    def add_child(self, move, father):
        nc = Node(self.board, self.ia, move, father, self.color)
        self.children.append(nc)

    def select_child_expand(self):
        if len(self.children) > 0:
            s = sorted(self.children, key=lambda c:
                       c.proba + Node.UCTK*sqrt(2*log(self.expansions)/c.expansions))[-1]
            if s is not None:
                if s.move is not None:
                    print("Node selected : " + str(s.move) + ", " +
                          str(s.proba + Node.UCTK*sqrt(2*log(self.expansions)/s.expansions)))
            else:
                print("Move is not None")
            return s
        else:
            return None

    def expand_node(self):
        if len(self.children) == 0:
            moves = self.get_moves_list()
            nb = self.board.get_legal_moves_play_list(moves)
            for m in nb:
                self.add_child((-self.move[0], m[0], m[1]), self)
            self.update_proba()
            self.update_expansion(len(nb))

            # print("Added " + str(nb))
        else:
            self.select_child_expand().expand_node()

    def get_moves_list(self):
        if self.father is not None:
            return [self.move] + self.father.get_moves_list()
        else:
            return []

    def compute_ia_proba(self):
        moves = self.get_moves_list()
        self.proba = self.ia.get_proba(self.board.get_matrix_play_list(moves))

    def update_proba(self):
        if len(self.children) == 0:
            self.compute_ia_proba()
        else:
            for c in self.children:
                self.min_max(c.proba)

    def min_max(self, proba):
        if self.move[0] == self.color:
            if proba > self.proba:
                self.proba = proba
                if self.father is not None:
                    self.father.update_proba()
        else:
            if proba < self.proba:
                self.proba = proba
                if self.father is not None:
                    self.father.update_proba()

    def update_expansion(self, nb):
        self.expansions += nb
        if self.father is not None:
            self.father.update_expansion(nb)


class UCT:
    def __init__(self, ia, **kwargs):
        self.ia = ia

        seconds = kwargs.get('time', 1)
        self.calculation_time = datetime.timedelta(seconds=seconds)

    def next_turn(self, board, color):
        root = Node(board, self.ia, None, None, color)

        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            root.expand_node()
            print("Node expanded !")


