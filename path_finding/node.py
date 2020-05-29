from data_processing.data import data as dt


class node:

    def __init__(self, row: int, col: int, data: dt) -> None:
        """ node cls holds the row and col values of a point on the grid """
        self.row = row
        self.col = col
        """isblocked == 1 means the node/grid is blocked"""
        self.index = data.to_index(self.row, self.col, data.cols)
        self.is_blocked = data.obstacles_arr[self.index] if (self.row < data.rows and self.col < data.cols) else None

        """ isNone is used for the padded nodes to reach the border vertices, otw the algorithm would avoid going to the boundary"""
        self.isNone: bool = True if self.is_blocked is None else False

    @classmethod
    def create(cls, row: int, col: int, data: dt):
        """Create a node or return None if the row and col provided are invalid"""
        if not (data.rows >= row >= 0 and data.cols >= col >= 0):
            return None

        return cls(row, col, data)

    def __eq__(self, other):
        if self is None and other is None:
            raise Exception("Possible? ")

        elif self is None and other.node_a is not None:
            raise Exception("Possible? ")
            return False

        elif self is not None and other is None:
            return False

        return self.row == other.row and self.col == other.col

    def __add__(self, other):
        if self is None and other is None:
            raise Exception("Possible? ")

        elif self is None and other is not None:
            raise Exception("Possible? ")
            return other.row, other.col

        elif self is not None and other is None:
            return self.row, self.col

        # print ((self.row, self.col) + (other.row, other.col))
        return (self.row, self.col) + (other.row, other.col)

    def __repr__(self) -> str:
        if self is None:
            return ""

        return f" row_col: {(self.row, self.col)}"
