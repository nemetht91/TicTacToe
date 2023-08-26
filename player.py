from mark import Mark
import numpy as np
import random
from game_logic import GameLogic


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
    def __init__(self, mark: Mark, game: GameLogic):
        super().__init__("Computer", mark)
        self.game = game
        self.difficulty = 0
        self.gpu_started = False
        self.gpu_last_move = None

    def place_mark(self):
        self.gpu_last_move = self._decision()
        return self.gpu_last_move

    def _decision(self):
        if self._is_first_round():
            return self._first_move()
        if self._is_second_round():
            return self._second_move()

    def _is_first_round(self):
        if self.game.mark_counter <= 1:
            return True
        return False

    def _is_second_round(self):
        if 2 <= self.game.mark_counter <= 3:
            return True
        return False

    def _first_move(self):
        if self._is_gpu_starts():
            return self._place_in_random_corner()
        return self._first_counter_move()

    def _second_move(self):
        if self.gpu_started:
            if self._is_last_center():
                return self._place_opposite_corner()
            return self._place_in_neighbour_corner()

    def _is_gpu_starts(self):
        if self.game.mark_counter == 0:
            self.gpu_started = True
        else:
            self.gpu_started = False
        return self.gpu_started

    def _first_counter_move(self):
        if self._is_last_center():
            return self._place_in_random_corner()
        return self._place_in_center()

    def _is_last_corner(self):
        last_move = [self.game.last_mark.row, self.game.last_mark.column]
        print(f"Last move: {last_move}")
        corners = [[0, 0], [0, 2], [2, 0], [2, 2]]
        is_corner = [corner == last_move for corner in corners]
        return np.any(is_corner)

    def _is_last_center(self):
        last_move = [self.game.last_mark.row, self.game.last_mark.column]
        center = [1, 1]
        return last_move == center

    def _place_opposite_corner(self):
        if self.gpu_last_move == (0, 0):
            return 2, 2
        if self.gpu_last_move == (0, 2):
            return 2, 0
        if self.gpu_last_move == (2, 0):
            return 0, 2
        return 0, 0

    def _place_in_neighbour_corner(self):
        free_corners = self._get_free_corner()
        print(free_corners)
        for corner in free_corners:
            if self._is_neighbour(self.gpu_last_move, corner) and self._is_empty_between(self.gpu_last_move, corner):
                return corner[0], corner[1]
        raise GpuPlayerException('Decision making error: Failed to place in neighbouring corner', 10)

    @staticmethod
    def _place_in_center():
        return 1, 1

    @staticmethod
    def _place_in_random_corner():
        corner_ids = [0, 2]
        row_id = random.choice(corner_ids)
        column_id = random.choice(corner_ids)
        return row_id, column_id

    def _is_free(self, row, column):
        return self.game.grid[row, column] == 0

    def _get_free_corner(self):
        corners = [[0, 0], [0, 2], [2, 0], [2, 2]]
        free_corners = []
        for corner in corners:
            if self._is_free(corner[0], corner[1]):
                free_corners.append(corner)
        return free_corners

    @staticmethod
    def _is_neighbour(corner1, corner2):
        if corner1[0] == corner1[1] and corner2[0] == corner2[1]:
            return False
        if corner1[0] != corner1[1] and corner2[0] != corner2[1]:
            return False
        return True

    def _is_empty_between(self, corner1, corner2):
        if corner1[0] == corner2[0]:
            row = self.game.grid[corner1[0], :]
            return row[1] == 0
        column = self.game.grid[:, corner1[1]]
        return column[1] == 0


class GpuPlayerException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)

        self.errors = errors


test_game = GameLogic(3)
test_computer = GpuPlayer(2, test_game)
gpu_first = test_computer.place_mark()
print(f"GPU first move: {gpu_first}")
test_game.add_mark(2, gpu_first[0], gpu_first[1])
test_game.add_mark(1, 1, 0)
gpu_second = test_computer.place_mark()
print(f"GPU second move: {gpu_second}")
test_game.add_mark(2, gpu_second[0], gpu_second[1])
