import sys
sys.path.insert(0, sys.path[0][0:-3]) #added

from board import Board
import numpy as np


WHITE = -1
BLACK = 1 # begins
BOARD_SIZE = 11


class IllegalMove(Exception):
    pass


class HexBoard(Board):
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
                raise IllegalMove
        else:
            raise IllegalMove

        line = []
        nl = []
        if move[0] == WHITE:
            for i in range(self.board_size):
                if self.matrix[0][i] == WHITE:
                    line.append(i)

            for i in range(1, self.board_size):
                if len(line) == 0:
                    break

                for l in line:
                    for j in range(max(0, l-1), min(self.board_size, l+1)):
                        if self.matrix[i][j] == WHITE:
                            nl.append(j)

                line = nl
                nl = []

            if len(line) > 0:
                self.win = WHITE

        else:
            for i in range(self.board_size):
                if self.matrix[i][0] == BLACK:
                    line.append(i)

            for i in range(1, self.board_size):
                if len(line) == 0:
                    break

                for l in line:
                    for j in range(max(0, l-1), min(self.board_size, l+1)):
                        if self.matrix[j][i] == BLACK:
                            nl.append(j)

                line = nl
                nl = []

            if len(line) > 0:
                self.win = BLACK

    def isWinner(self, player):
        win = False
        if self.win == player:
            win = True
        return win



