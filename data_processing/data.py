import math
import geopandas
import numpy as np
from functools import reduce
from collections.abc import Iterable


class data:
    def __init__(self, sqr_grid_length, sqr_grid_length_pad, threshold, data_file_path) -> None:

        """ user provided values"""
        self.threshold = threshold
        self.sqr_grid_length = sqr_grid_length
        self.sqr_grid_length_pad = sqr_grid_length_pad

        """ Read shape file using geopanda as a dataframe """
        self.crime_data = geopandas.read_file(data_file_path)

        """  Extract all the points from the data frame as a list of points """
        self.x_y_pair = list(map(lambda point: list(point.coords)[0], self.crime_data.geometry))
        self.x = list(map(lambda point: point[0], self.x_y_pair))
        self.y = list(map(lambda point: point[1], self.x_y_pair))

        """ To draw the grids: identifying the bounds of the given data s"""
        self.min_x = min(self.x)
        self.min_y = min(self.y)
        self.max_x = max(self.x)
        self.max_y = max(self.y)

        # FIXME : Final clean
        # GTK: Alternative of finding min and max of x and y using pandas
        # By creating a polygon using all the crime data points
        # poly = polygon(x_y_pair)
        # bounds = poly.bounds
        # print("bounds: (minx-0, miny-1, maxx-2, maxy-3) ", bounds)

        """ To draw the grids: calculating required rows and cols, NOTE: rows -> are y and cols are x """
        self.cols = int(math.ceil(abs(abs(self.max_x) - abs(self.min_x)) / self.sqr_grid_length))
        self.rows = int(math.ceil(abs(abs(self.max_y) - abs(self.min_y)) / self.sqr_grid_length))

        """ To get perfect square grids: calculating the bounds """
        self.lower_x_bound = self.min_x
        self.upper_x_bound = self.min_x + (self.cols * self.sqr_grid_length)
        self.lower_y_bound = self.min_y
        self.upper_y_bound = self.min_y + (self.rows * self.sqr_grid_length)

        """ To draw the grids:, generating the x and y points of the grids """
        self.col_points = list(
            np.arange(self.min_x, (self.upper_x_bound + (self.sqr_grid_length / 3)), self.sqr_grid_length))

        self.row_points = list(
            np.arange(self.min_y, (self.upper_y_bound + (self.sqr_grid_length / 3)), self.sqr_grid_length))

        """ To draw initial purple patches: calculate the rectangular grid length & width """
        self.max_y_length = abs(abs(self.upper_y_bound) - abs(self.min_y))
        self.max_x_length = abs(abs(self.upper_x_bound) - abs(self.min_x))

        """ To create crime rate matrix: Calculate the axis offsets """
        self.x_offset = 0 - self.min_x
        self.y_offset = 0 - self.min_y

        """ To create crime rate matrix: Calculate offset values of x and y and identify the crime coord. to corresponding grids """
        self.grid_row, self.grid_col = self.to_row_col_from_coord(self.x, self.y)

        """ To create crime rate matrix: Calculate matrix size and generate empty matrix """
        self.number_of_grids = self.rows * self.cols
        self.crime_rate_arr = np.zeros(self.number_of_grids, dtype=int)

        """ Sorted crime rate array to determine threshold """
        self.crime_rate_arr_sorted = None

        """ Statistics """
        self.median = None
        self.average = None
        self.std_dev = None

        """Obstacles array identifies the blocked and non-blocked grids"""
        self.threshold_val = None
        self.obstacles_arr = None

        self.total_path_costs: tuple = None
        self.max_of_heuristic_calc: float = None
        self.path_found: bool = False
        self.time_taken = None

        # FIXME: Final clean (Not required) Fix the functions to store the data as file
        # Store file/Save files
        # To save crime data as CSV format to read the data
        # self.crime_data.to_csv("".join([figure_dir_path, "crime_data.csv"]), index=True)

        # To save coordinate data as CSV format to read the data
        # output = np.column_stack((np.array(x).flatten(), np.array(y).flatten()))
        # np.savetxt("".join([figures_dir_path, "output.csv"]), output, delimiter=",")

    """Updating crime matrix with number of crimes occurred corresponding to grids"""

    def update_crime_rate_array(self):
        if self.grid_col.__len__() != self.grid_row.__len__():
            print("Quiting, Something went wrong with the coordinates")
            quit(-1)

        for i in range(0, self.grid_row.__len__()):
            self.crime_rate_arr[self.to_index(self.grid_row[i], self.grid_col[i], self.cols)] += 1

    """Sort crime array for threshold in descending order"""

    def sort_crime_data_array(self):
        self.crime_rate_arr_sorted = np.sort(self.crime_rate_arr)[::-1]

    """Calculating crime statistics"""

    def calculate_statistics(self):
        self.median = np.median(self.crime_rate_arr_sorted)
        self.average = np.average(self.crime_rate_arr_sorted)
        self.std_dev = np.std(self.crime_rate_arr_sorted)

    """Updating blocked and non-blocked areas on matrix"""

    def update_obstacles_arr(self):
        self.sort_crime_data_array()
        self.median = np.median(self.crime_rate_arr_sorted)
        self.obstacles_arr = self.crime_rate_arr.copy()

        if self.threshold == 50:
            self.threshold_val = self.median
        else:
            max_blocked_index = math.floor(self.number_of_grids * (1 - (self.threshold / 100)))
            max_blocked_index = 1 if (max_blocked_index <= 0) else max_blocked_index

            self.threshold_val = self.crime_rate_arr_sorted[max_blocked_index - 1]

            self.threshold_val = max(self.crime_rate_arr_sorted) + 1 if (self.threshold == 100) else self.threshold_val

        for i in range(0, self.obstacles_arr.__len__()):
            if self.obstacles_arr[i] >= self.threshold_val:
                # Blocked
                self.obstacles_arr[i] = 1
            else:
                # Open
                self.obstacles_arr[i] = 0

    """ Helper function to move between row_col and coordinates of the grid"""

    def to_index(self, row: int, col: int, cols):
        return (row * cols) + col

    def to_row_col_from_index(self, index, cols):
        return divmod(index, cols)

    """To create crime rate matrix: Calculate offset values of x and y and identify the crime coord. to corresponding grids"""

    def to_row_col_from_coord(self, x, y):
        if isinstance(x, Iterable) and isinstance(y, Iterable):
            x_normalized = np.array(x) + self.x_offset
            y_normalized = np.array(y) + self.y_offset
            # Or using numpy to get the same effect
            # x_offset = list(map(lambda x_val: x_val + x_axis_offset, x))
            # y_offset = list(map(lambda y_val: y_val + y_axis_offset, y))
            grid_col = np.array(x_normalized // self.sqr_grid_length, dtype=int)
            grid_row = np.array(y_normalized // self.sqr_grid_length, dtype=int)

            return grid_row, grid_col

        x_normalized = x + self.x_offset
        y_normalized = y + self.y_offset
        grid_col = x_normalized // self.sqr_grid_length
        grid_row = y_normalized // self.sqr_grid_length
        return int(grid_row), int(grid_col)

    def to_coordinate_from_row_col(self, row_col: tuple):
        row_coord = (self.lower_x_bound + row_col[1] * self.sqr_grid_length)
        col_coord = (self.lower_y_bound + row_col[0] * self.sqr_grid_length)
        return row_coord, col_coord

    """ Print out function definitions """

    def obstacles_matrix_readable(self):
        return np.flipud(self.obstacles_arr.reshape(self.rows, self.cols))

    def crime_rate_matrix_readable(self):
        return np.flipud(self.crime_rate_arr.reshape(self.rows, self.cols))

    def crime_rate_matrix(self):
        return self.crime_rate_arr.reshape(self.rows, self.cols)

    def obstacle_matrix(self):
        return self.obstacles_arr.reshape(self.rows, self.cols)

    def iterate_crime_rate_matrix(self, cr_matrix, rows, cols):
        for m in range(0, rows):
            for n in range(0, cols):
                print(cr_matrix[m, n], end="  ")
            print(" ")

    def print(self):
        print(f"* Bounds: (minx: {self.min_x}, miny:{self.min_y}, maxx:{self.max_x}, maxy:{self.max_y}) ")
        # print("* column points: \n", self.col_points)
        # print("* row points: \n", self.row_points)
        # print("* crime data array: \n", self.crime_rate_arr)
        # print("* crime matrix: \n", self.crime_rate_matrix())
        print("* Crime matrix - readable-view: \n", self.crime_rate_matrix_readable())
        print(f"* For {50}% Threshold, The Threshold value is : ", self.threshold_val)
        print("* Crime data array sorted: \n", self.crime_rate_arr_sorted)
        # print("* crime rate matrix view: \n")
        # self.iterate_crime_rate_matrix(self.crime_rate_matrix_grid_matched(), self.rows, self.cols)
        print("* Median: ", self.median)
        print("* Average: ", self.average)
        print("* Standard Deviation: ", self.std_dev)
        print("* Obstacles array: ", self.obstacles_arr)
        print("* Obstacles Matrix - readable-view: ", self.obstacles_matrix_readable())
