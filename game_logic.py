import numpy as np


class Mark:
    def __init__(self):
        self.value = 0
        self.row = 0
        self.column = 0

    def set_mark(self, value, row, column):
        self.value = value
        self.row = row
        self.column = column


class GameLogic:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.cross = 1
        self.o = 2
        self.mark_counter = 0
        self.max_marks = grid_size**2
        self.last_mark = Mark()

    def reset_grid(self):
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.max_marks = 0

    def add_cross(self, row, column):
        return self._add_to_grid(self.cross, row, column)

    def add_o(self, row, column):
        return self._add_to_grid(self.o, row, column)

    def _add_to_grid(self, value, row, column):
        if not self._is_valid(row, column):
            return False
        if self._get_current_value(row, column) != 0:
            return False
        self.grid[row, column] = value
        self.mark_counter += 1
        self.last_mark.set_mark(value, row, column)
        return True

    def _is_valid(self, row, column):
        if 0 > row > self.grid_size:
            return False
        if 0 > column > self.grid_size:
            return False
        return True

    def _get_current_value(self, row, column):
        return self.grid[row, column]

    def is_grid_full(self):
        if self.mark_counter >= self.max_marks:
            return True
        return False

    def is_won(self):
        if self.is_row_won() or self.is_column_won():
            return True
        if self.is_diagonal_won():
            return True
        return False

    def is_row_won(self):
        current_row = self.grid[self.last_mark.row, :]
        if np.all(current_row) == self.last_mark.value:
            return True
        return False

    def is_column_won(self):
        current_column = self.grid[:, self.last_mark.column]
        if np.all(current_column) == self.last_mark.value:
            return True
        return False

    def is_diagonal_won(self):
        if not self.is_on_diagonal():
            return False
        diagonal = self.grid.diagonal()
        flipped_diagonal = np.fliplr(self.grid).diagonal()
        if np.all(diagonal) == self.last_mark.value:
            return True
        if np.all(flipped_diagonal) == self.last_mark.value:
            return True
        return False

    def is_on_diagonal(self):
        if self.last_mark.row == self.last_mark.column:
            return True
        if self.last_mark.row == 0 and self.last_mark.column == self.grid_size-1:
            return True
        if self.last_mark.column == 0 and self.last_mark.row == self.grid_size-1:
            return True
        return False

    def print_grid(self):
        print(self.grid)


game = GameLogic(3)
game.add_cross(0, 2)
game.add_cross(1, 1)
game.add_cross(2, 0)
game.print_grid()
game.is_grid_full()
print(game.is_won())