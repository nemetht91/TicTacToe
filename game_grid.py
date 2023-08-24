
class GameGrid:
    def __init__(self, rows, columns, row_offset, column_offset, block_width, block_height, frame_width):
        self.rows = rows
        self.columns = columns
        self.row_offset = row_offset
        self.column_offset = column_offset
        self.block_width = block_width
        self.block_height = block_height
        self.frame_width = frame_width

    def which_block(self, x, y):
        x = x - self.row_offset
        y = y - self.column_offset
        if not self._is_on_block(x, y):
            return None
        row = x // (self.block_width + self.frame_width)
        column = y // (self.block_height + self.frame_width)
        block = (row, column)
        return block

    def _is_on_block(self, x, y):
        if not self._is_on_grid(x, y):
            return False
        if self._is_on_frame(x, self.block_width, self.rows):
            return False
        if self._is_on_frame(y, self.block_height, self.columns):
            return False
        return True

    def _is_on_frame(self, coord, grid_dimension, grid_size):
        block_size = self.frame_width + grid_dimension
        for i in range(grid_size):
            if grid_dimension + i * block_size <= coord <= (i + 1) * block_size:
                return True
        return False

    def _is_on_grid(self, x, y):
        if 0 > x > self.max_width():
            return False
        if 0 > y > self.max_height():
            return False
        return True

    def max_width(self):
        return self.rows * (self.block_width + self.frame_width) - self.frame_width

    def max_height(self):
        return self.columns * (self.block_height + self.frame_width) - self.frame_width

    def get_block_center(self, row, column):
        x_cord = (1 + 2 * row) * self.block_width/2 + row * self.frame_width + self.row_offset
        y_cord = (1 + 2 * column) * self.block_height/2 + column * self.frame_width + self.column_offset
        return x_cord, y_cord

