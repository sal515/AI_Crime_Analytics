import math
from functools import total_ordering
from data_processing.data import data as dt


# @total_ordering
class node:

    def __init__(self, x: float, y: float, data: dt) -> None:
        self.row, self.col = data.to_row_col_from_coord(x, y)
        self.x, self.y = data.to_coordinate_from_row_col((self.row, self.col))

        print(self.row, self.col)

        self.is_blocked = data.obstacles_arr[data.to_index(self.row, self.col, data.cols)]

    def __eq__(self, other):
        # if other is not None:
        return self.row == other.row and self.col == other.col

    def __add__(self, other):
        return (self.row, self.col) + (other.row, other.col)

    def __repr__(self) -> str:
        return f"x_y: {(self.x, self.y)}, row_col: {(self.row, self.col)}"

    # def __hash__(self):
    #     return hash(self.position)
