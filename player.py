from mark import Mark
import numpy as np
import random


class Player:
    def __init__(self, name, mark: Mark):
        self.name = name
        self.mark = mark
        self.score = 0

    def increment_score(self):
        self.score += 1

    def reset_score(self):
        self.score = 0


class GpuPlayer(Player):
    def __init__(self, mark: Mark, grid):
        super.__init__("Computer", mark)
        self.grid = grid
        self.difficulty = 0


