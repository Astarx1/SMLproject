from parameters import Params
from ia import IA

import os
import time
import random
import numpy as np
import sys
sys.path.append('..')
from .hex_NNet import HexNet as hnet
from .hex_board import BOARD_SIZE


class dotdict(dict):
    def __getattr__(self, name):
        return self[name]


args = dotdict({
    'lr': 0.001,
    'dropout': 0.3,
    'epochs': Params.EPOCS,
    'batch_size': Params.BATCH_SIZE,
    'cuda': Params.CUDA,
    'num_channels': Params.NUMBER_FILTERS,
})


class HexIA(IA):
    compute_proba_time = 0

    def __init__(self, specific_args=None, load_checkpoint=False):
        if specific_args is None:
            self.nnet = hnet(args)
        if load_checkpoint:
            self.load_checkpoint()

    def train(self, examples):
        """
        examples: list of examples, each example is of form (board, pi, v)
        """
        inputs = list(zip(*examples))
        input_boards = np.asarray(inputs[0])
        target_pis = np.asarray(inputs[1])
        target_vs = np.asarray(inputs[2])
        self.nnet.model.fit(x=input_boards, y=[target_pis, target_vs], batch_size=args.batch_size, epochs=args.epochs)

    def get_proba(self, board):
        """
        board: np array with board
        """
        board = board[np.newaxis, :, :]
        pi, v = self.nnet.model.predict(board)
        return pi[0], v[0]

    def save_checkpoint(self, folder=Params.NN_CHECKPOINT_FOLDER, filename=Params.NN_CHECKPOINT_FILENAME):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        self.nnet.model.save_weights(filepath)

    def load_checkpoint(self, folder=Params.NN_CHECKPOINT_FOLDER, filename=Params.NN_CHECKPOINT_FILENAME):
        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            raise("No model in path {}".format(filepath))
        self.nnet.model.load_weights(filepath)


class HexIARandom(IA):
    def __init__(self):
        random.seed(1)
        IA.__init__(self)

    def get_proba(self, matrix):
        t = 0.5 + 0.1*(random.random()-0.5)
        p = np.ones((BOARD_SIZE*BOARD_SIZE))
        return p, t

