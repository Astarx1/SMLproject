from ia import IA
import random


class HexIA(IA):
    def __init__(self):
        random.seed(1)
        IA.__init__(self)

    def get_proba(self, matrix):
        t = 0.5 + 0.1*(random.random()-0.5)
        return t

