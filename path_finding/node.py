import math
from functools import total_ordering
from data_processing.data import data as dt


# @total_ordering
class node:

    def __init__(self, row: int, col: int, data: dt) -> None:
        self.row = row
        self.col = col
        # self.x, self.y = data.to_coordinate_from_row_col((self.row, self.col))
        # print(self.row, self.col)

        self.is_blocked = data.obstacles_arr[data.to_index(self.row, self.col, data.cols)]

    @classmethod
    def create(cls, row: int, col: int, data: dt):
        """Create a node or return None if the row and col provided are invalid"""
        if not (data.rows > row >= 0 and data.cols > col >= 0):
            return None
        return cls(row, col, data)

    def __eq__(self, other):
        if self is None and other is None:
            raise Exception("Possible? ")
        elif self is None and other.node_a is not None:
            return False
        elif self is not None and other is None:
            return False

        return self.row == other.row and self.col == other.col

    def __add__(self, other):
        if self is None and other is None:
            raise Exception("Possible? ")
        elif self is None and other is not None:
            return other.row, other.col
        elif self is not None and other is None:
            return self.row, self.col
        # print ((self.row, self.col) + (other.row, other.col))
        return (self.row, self.col) + (other.row, other.col)

    def __repr__(self) -> str:
        if self is None:
            return ""
        return f" row_col: {(self.row, self.col)}"

    # def __hash__(self):
    #     return hash(self.position)
