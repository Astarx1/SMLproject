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
                raise IllegalMove
        else:
            raise IllegalMove

    def find_if_winner(self, move):
        cur_line = []
        nl = []
        if move[0] == WHITE:
            cur_line.append([])
            for i in range(self.board_size):
                if self.matrix[0][i] == WHITE:
                    #print("init : " + str(i))
                    (cur_line[0]).append(i)

            for i in range(1, self.board_size):
                if len(cur_line[i-1]) == 0:
                    break

                cur_line.append([])
                neighbors = []
                #print("Looking for neighbors in line " + str(i-1) + " : " + str(cur_line[i-1]))
                for y in cur_line[i-1]:
                    if y > 0:
                        if self.matrix[i-1][y-1] == WHITE and y-1 not in cur_line[i-1]:
                            #print("found neighbour line " + str(i) + " : " + str(y-1))
                            neighbors.append(y-1)
                    if y+1 < BOARD_SIZE:
                        if self.matrix[i-1][y+1] == WHITE and y+1 not in cur_line[i-1]:
                            #print("found neighbour line " + str(i) + " : " + str(y+1))
                            neighbors.append(y+1)
                cur_line[i-1] = neighbors + cur_line[i-1]

                #print("Looking for points from line " + str(i-1) + " : " + str(cur_line[i-1]))
                for y in cur_line[i-1]:
                    if self.matrix[i][y] == WHITE and y not in cur_line[i]:
                        #print("found point line " + str(i) + " : " + str(y))
                        cur_line[i].append(y)
                    if y+1 < BOARD_SIZE:
                        if self.matrix[i][y+1] == WHITE and y+1 not in cur_line[i]:
                            #print("found point line " + str(i) + " : " + str(y+1))
                            cur_line[i].append(y+1)


                #print("Result -> line " + str(i) + " : " + str(cur_line[i]))

            if len(cur_line) > 10:
                self.win = WHITE

        else:
            cur_line.append([])
            for i in range(self.board_size):
                if self.matrix[i][0] == BLACK:
                    #print("init : " + str(i))
                    (cur_line[0]).append(i)

            for i in range(1, self.board_size):
                if len(cur_line[i-1]) == 0:
                    break

                cur_line.append([])
                neighbors = []
                #print("Looking for neighbors in line " + str(i-1) + " : " + str(cur_line[i-1]))
                for x in cur_line[i-1]:
                    if x > 0:
                        if self.matrix[x-1][i-1] == BLACK and x-1 not in cur_line[i-1]:
                            #print("found neighbour line " + str(i) + " : " + str(x-1))
                            neighbors.append(x-1)
                    if x+1 < BOARD_SIZE:
                        if self.matrix[i-1][x+1] == BLACK and x+1 not in cur_line[i-1]:
                            #print("found neighbour line " + str(i) + " : " + str(x+1))
                            neighbors.append(x+1)
                cur_line[i-1] = neighbors + cur_line[i-1]

                #print("Looking for points from line " + str(i-1) + " : " + str(cur_line[i-1]))
                for x in cur_line[i-1]:
                    if self.matrix[x][i] == BLACK and x not in cur_line[i]:
                        #print("found point line " + str(i) + " : " + str(x))
                        cur_line[i].append(x)
                    if x+1 < BOARD_SIZE:
                        if self.matrix[x+1][i] == BLACK and x+1 not in cur_line[i]:
                            #print("found point line " + str(i) + " : " + str(x+1))
                            cur_line[i].append(x+1)


                #print("Result -> line " + str(i) + " : " + str(cur_line[i]))

            if len(cur_line) > 10:
                self.win = BLACK

    def isWinner(self, player):
        win = False
        if self.win == player:
            win = True
        return win

    def __str__(self):
        return str(np.rot90(self.matrix, 1))

