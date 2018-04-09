import copy
import numpy as np
from parameters import Params


INIT_BOARD_SIZE = Params.BOARD_SIZE


class Board:
    def __init__(self, board_size):
        self.board_size = board_size
        self.matrix = np.zeros((board_size, board_size), dtype=int)
        self.win = 0
        self.moves_list = []

    @staticmethod
    def get_init_board():
        return np.zeros((INIT_BOARD_SIZE, INIT_BOARD_SIZE), dtype=int)

    @staticmethod
    def get_canonical_board(board, player):
        return player*board

    def get_clone(self):
        return copy.deepcopy(self)

    def next_legal_moves(self):
        pass

    def play_move(self, move):
        pass

    def play_list(self, move_list):
        pass

    def winner(self):
        return self.win

    def get_repr_matrix(self):
        return self.matrix

    def get_copy_matrix(self):
        return self.matrix.copy()

    def get_legal_moves_play_list(self, move_list):
        matrix_save = np.copy(self.matrix)

        if move_list is not None:
            for m in move_list:
                self.play_move(m)

        r = self.next_legal_moves()
        self.matrix = matrix_save
        return r

    def get_matrix_play_list(self, move_list):
        matrix_save = np.copy(self.matrix)

        if move_list is not None:
            for m in move_list:
                self.play_move(m)

        r = self.get_repr_matrix().copy()
        self.matrix = matrix_save
        return r

    @staticmethod
    def board_to_array(matrix):
        return matrix.flatten()

    @staticmethod
    def array_to_board(array):
        array = array.reshape((INIT_BOARD_SIZE, INIT_BOARD_SIZE))
        return array
