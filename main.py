# -------------------------------------------------------
# Assignment 1
# FIXME: Add student id
# Written by Salman Rahman <Student id here don't forget>
# For COMP 472 Section - ABIX – Summer 2020
# --------------------------------------------------------

# TODO: Move functions to separate package
# ====== functions ======
import math


def iterate_cr_matrix(cr_matrix, rows, cols):
    for m in range(0, rows):
        for n in range(0, cols):
            print(cr_matrix[m, n], end="    ")
        print(" ")


def save_figure(plt, figureName):
    plt.savefig("".join([figures_dir_path, figureName]))


# ====== imports ======
import geopandas
import matplotlib.axes as axes
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import Polygon as polygon
from shapely.geometry import MultiPoint
from shapely.geometry import Point
import numpy as np
from functools import reduce

# ====== user input variables ======
square_grid_length = 0.002
grid_buffer = square_grid_length * 2

# ====== constant path variables ======
shapes_data_path = "data\\Shape\\crime_dt.shp"
figures_dir_path = "figures\\"

# ====== logic ======

# Read shape file using geopanda as a dataframe
crime_data = geopandas.read_file(shapes_data_path)
# To save crime data as CSV format to read the data
# crime_data.to_csv("".join([figures_dir_path, "crime_data.csv"]), index=True)

# Extract all the points from the data frame as a list of points
x_y_pair = list(map(lambda point: list(point.coords)[0], crime_data.geometry))
x = list(map(lambda point: point[0], x_y_pair))
y = list(map(lambda point: point[1], x_y_pair))
# To save coordinate data as CSV format to read the data
# output = np.column_stack((np.array(x).flatten(), np.array(y).flatten()))
# np.savetxt("".join([figures_dir_path, "output.csv"]), output, delimiter=",")

# To draw the grids: identifying the bounds of the given data
# By creating a polygon using all the crime data points
min_x = min(x)
min_y = min(y)
max_x = max(x)
max_y = max(y)
print(f"bounds: (minx:{min_x}, miny:{min_y}, maxx:{max_x}, maxy:{max_y}) ")

# poly = polygon(x_y_pair)
# bounds = poly.bounds
# print("bounds: (minx-0, miny-1, maxx-2, maxy-3) ", bounds)

# To draw the grids: calculating required rows and cols
cols = int(math.ceil(abs(abs(max_x) - abs(min_x)) / square_grid_length))
rows = int(math.ceil(abs(abs(max_y) - abs(min_y)) / square_grid_length))

# To get perfect square grids: calculating the bounds
lower_x_bound = min_x
upper_x_bound = min_x + (cols * square_grid_length)
lower_y_bound = min_y
upper_y_bound = min_y + (rows * square_grid_length)

# To draw the grids:, generating the x and y points of the grids
col_points = list(
    np.arange(min_x, (upper_x_bound + (square_grid_length / 3)), square_grid_length))

row_points = list(
    np.arange(min_y, (upper_y_bound + (square_grid_length / 3)), square_grid_length))

print("column points: ", col_points)
print("row points: ", row_points)

# To draw initial purple patch: calculate the rectangular grid length & width
max_y_length = abs(abs(upper_y_bound) - abs(min_y))
max_x_length = abs(abs(upper_x_bound) - abs(min_x))

# For visualization: Generate a figure with all the data shown
# crime_data.geometry.plot(ax=ax)
fig1 = plt.figure(1)
ax = fig1.add_subplot(1, 1, 1)

# To view the plot easily: Set axis bounds with buffer around edges
plt.axis([(min(x) - grid_buffer), (max(x) + grid_buffer), (min(y) - grid_buffer), (max(y) + grid_buffer)])

rect_initial = patches.Rectangle((min(x), min(y)), max_x_length, max_y_length, color="purple")
ax.add_patch(rect_initial)

# To view the data: Plot points
plt.plot(x, y, ".")

# To view the grids: Drawing lines vertical and horizontal
for i in col_points:
    plt.axvline(x=i)
for i in row_points:
    plt.axhline(y=i)
# TODO: figure out why lambda doesn't work
# map(lambda col: plt.axvline(x=col), col_points)

# FIXME: Fix the grid lines to span only on the data points area
# start_point = [col_points[3], row_points[0]]
# end_point = [col_points[3], row_points[(row_points.__len__() - 1)]]
# plt.plot(start_point, end_point)

# To create crime rate matrix: Calculate the axis offsets
x_axis_offset = 0 - min_x
y_axis_offset = 0 - min_y

# To create crime rate matrix: Calculate offset values of x and y
# x_offset = list(map(lambda x_val: x_val + x_axis_offset, x))
# y_offset = list(map(lambda y_val: y_val + y_axis_offset, y))
# Or using numpy to get the same effect
x_offset = np.array(x) + x_axis_offset
y_offset = np.array(y) + y_axis_offset

# To create crime rate matrix: Identify the crime coord. to corresponding grids
grid_row = np.array(x_offset // square_grid_length, dtype=int)
grid_col = np.array(y_offset // square_grid_length, dtype=int)

# To create crime rate matrix: Calculate matrix size and generate empty matrix
cr_mat_sz = rows * cols
cr_matrix = np.zeros(cr_mat_sz, dtype=int)

# Updating crime matrix with number of crimes occurred corresponding to grids
grid_row_sz = grid_row.__len__()
grid_col_sz = grid_col.__len__()
if grid_row_sz != grid_col_sz:
    print("Quit, Something went wrong with the coordinates")
    quit(-1)

for i in range(0, grid_row_sz):
    # index = (grid_row[i] * rows) + grid_col[i]
    index = (grid_col[i] * cols) + grid_row[i]
    cr_matrix[index] += 1

print(cr_matrix)

# Visualize updated matrix of crime rates
# print("not flipped")
# print((cr_matrix.reshape(rows, cols)).view(type=np.matrix))
print("flipped to match grid")
cr_matrix_flipped = np.flipud(cr_matrix.reshape(rows, cols)).view(type=np.matrix)
print(cr_matrix_flipped)

# Test grid counts

iterate_cr_matrix(cr_matrix_flipped, rows, cols)

# To visualize high risk grids: Add yellow rectangles
rect_high_risk = patches.Rectangle((min(x), min(y)), square_grid_length, square_grid_length, color="red")
ax.add_patch(rect_high_risk)

risky_grid = (min(x), min(y))

rect_high_risk = patches.Rectangle(risky_grid, square_grid_length, square_grid_length, color="yellow")
ax.add_patch(rect_high_risk)

# Display plot
save_figure(plt, "all_crime_data.png")
plt.show()

# ===== end of program =====
print("=== program terminated ===")
