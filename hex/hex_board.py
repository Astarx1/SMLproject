import sys
sys.path.insert(0, sys.path[0][0:-3]) #added

from board import Board
from parameters import Params

import numpy as np


WHITE = Params.WHITE
BLACK = Params.BLACK  # begins
BOARD_SIZE = Params.BOARD_SIZE


class IllegalMove(Exception):
    pass


class HexBoard(Board):
    upward_pattern = ((0, 1), (1, 1))
    upward_neighbors = ((1, 0), (-1, 0))

    def __init__(self):
        Board.__init__(self, BOARD_SIZE)

    @staticmethod
    def get_init_board():
        return np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

    def next_legal_moves(self):
        moves = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.matrix[i][j] == 0:
                    moves.append([i, j])
        return moves

    def play_move(self, move):
        if self.board_size > move[1] >= 0 and self.board_size > move[2] >= 0:
            if self.matrix[move[1]][move[2]] == 0:
                self.matrix[move[1]][move[2]] = move[0]
                self.moves_list.append(move)
            else:
                Params.log("hex_board.py", "Illegal move : " + str(move))
                raise IllegalMove
        else:
            Params.log("hex_board.py", "Illegal move : " + str(move))
            raise IllegalMove

    def find_if_winner(self, move):
        cur_line = []
        if move[0] == WHITE:
            cur_line.append([])
            for i in range(self.board_size):
                if self.matrix[0][i] == WHITE:
                    (cur_line[0]).append(i)

            for i in range(1, self.board_size):
                if len(cur_line[i - 1]) == 0:
                    break

                # look if there are neighbors on the same line
                cur_line.append([])
                stillSomeNeigh = True
                neighbors = []
                while stillSomeNeigh:
                    stillSomeNeigh = False
                    for y in cur_line[i - 1]:
                        if y > 0:
                            if self.matrix[i - 1][y - 1] == WHITE and y - 1 not in cur_line[i - 1]:
                                neighbors.append(y - 1)
                                stillSomeNeigh = True
                        if y + 1 < BOARD_SIZE:
                            if self.matrix[i - 1][y + 1] == WHITE and y + 1 not in cur_line[i - 1]:
                                neighbors.append(y + 1)
                                stillSomeNeigh = True
                    cur_line[i - 1] = neighbors + cur_line[i - 1]

                # look if there are neighbors on the next line
                for y in cur_line[i - 1]:
                    if self.matrix[i][y] == WHITE and y not in cur_line[i]:
                        cur_line[i].append(y)
                    if y + 1 < BOARD_SIZE:
                        if self.matrix[i][y + 1] == WHITE and y + 1 not in cur_line[i]:
                            cur_line[i].append(y + 1)

            if len(cur_line) is BOARD_SIZE:
                if len(cur_line[BOARD_SIZE - 1]) > 0:
                    self.win = WHITE

        else:
            cur_line.append([])
            for i in range(self.board_size):
                if self.matrix[i][0] == BLACK:
                    (cur_line[0]).append(i)

            for i in range(1, self.board_size):
                if len(cur_line[i - 1]) == 0:
                    break

                cur_line.append([])
                stillSomeNeigh = True
                neighbors = []
                while stillSomeNeigh:
                    stillSomeNeigh = False
                    for x in cur_line[i - 1]:
                        if x > 0:
                            if self.matrix[x - 1][i - 1] == BLACK and x - 1 not in cur_line[i - 1]:
                                neighbors.append(x - 1)
                                stillSomeNeigh = True
                        if x + 1 < BOARD_SIZE:
                            if self.matrix[i - 1][x + 1] == BLACK and x + 1 not in cur_line[i - 1]:
                                neighbors.append(x + 1)
                                stillSomeNeigh = True
                    cur_line[i - 1] = neighbors + cur_line[i - 1]

                for x in cur_line[i - 1]:
                    if self.matrix[x][i] == BLACK and x not in cur_line[i]:
                        cur_line[i].append(x)
                    if x + 1 < BOARD_SIZE:
                        if self.matrix[x + 1][i] == BLACK and x + 1 not in cur_line[i]:
                            cur_line[i].append(x + 1)

            if len(cur_line) is BOARD_SIZE:
                if len(cur_line[BOARD_SIZE - 1]) > 0:
                    self.win = BLACK

    def __str__(self):
        return str(np.rot90(self.matrix, 1))

