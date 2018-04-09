from keras.models import *
from keras.layers import *
from keras.optimizers import *
from keras.utils import *

from .hex_board import BOARD_SIZE


class HexNet:
    def __init__(self, args):
        self.board_size = BOARD_SIZE
        self.args = args

        # Neural Net
        self.input_boards = Input(shape=(self.board_size, self.board_size))  # s: batch_size x board_x x board_y

        x_image = Reshape((self.board_size, self.board_size, 1))(self.input_boards)  # batch_size x board_x x board_y

        # batch_size  x board_x x board_y x num_channels
        h_conv1 = Activation('relu')(BatchNormalization(axis=3)(Conv2D(args.num_channels, 3, padding='same')(x_image)))
        # batch_size  x board_x x board_y x num_channels
        h_conv2 = Activation('relu')(BatchNormalization(axis=3)(Conv2D(args.num_channels, 3, padding='same')(h_conv1)))
        # batch_size  x (board_x-2) x (board_y-2) x num_channels
        h_conv3 = Activation('relu')(BatchNormalization(axis=3)(Conv2D(args.num_channels, 3, padding='valid')(h_conv2)))
        # batch_size  x (board_x-4) x (board_y-4) x num_channels
        h_conv4 = Activation('relu')(BatchNormalization(axis=3)(Conv2D(args.num_channels, 3, padding='valid')(h_conv3)))

        h_conv4_flat = Flatten()(h_conv4)
        # batch_size x 1024
        s_fc1 = Dropout(args.dropout)(Activation('relu')(BatchNormalization(axis=1)(Dense(1024)(h_conv4_flat))))
        # batch_size x 1024
        s_fc2 = Dropout(args.dropout)(Activation('relu')(BatchNormalization(axis=1)(Dense(512)(s_fc1))))
        # batch_size x self.action_size
        self.pi = Dense(self.board_size*self.board_size, activation='softmax', name='pi')(s_fc2)
        # batch_size x 1
        self.v = Dense(1, activation='tanh', name='v')(s_fc2)

        self.model = Model(inputs=self.input_boards, outputs=[self.pi, self.v])
        self.model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=Adam(args.lr))

    def summary(self):
        print_summary(self.model, line_length=None, positions=None, print_fn=None)
