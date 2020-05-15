# -------------------------------------------------------
# Assignment 1
# FIXME: Add student id
# Written by Salman Rahman <Student id here don't forget>
# For COMP 472 Section - ABIX – Summer 2020
# --------------------------------------------------------

# TODO: Move functions to separate package
# ====== functions ======


def draw_blocked_grid(isOpen, index, cols, minx, miny, square_grid_length, ax, color="yellow"):
    if isOpen:
        return

    row_col = to_row_col(index, cols)

    risky_grid = (min(x) + row_col[1] * square_grid_length, min(y) + row_col[0] * square_grid_length)

    rect_high_risk = patches.Rectangle(risky_grid, square_grid_length, square_grid_length, color=color)
    ax.add_patch(rect_high_risk)


def to_index(row, col, cols):
    return (row * cols) + col


def to_row_col(index, cols):
    return divmod(index, cols)


def iterate_cr_matrix(cr_matrix, rows, cols):
    for m in range(0, rows):
        for n in range(0, cols):
            print(cr_matrix[m, n], end="  ")
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
import math

# ====== user input variables ======
square_grid_length = 0.002
grid_buffer = square_grid_length * 2

threshold = 50
# threshold = 20

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
# rows -> are y and cols are x
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
x_offset = 0 - min_x
y_offset = 0 - min_y

# To create crime rate matrix: Calculate offset values of x and y
# x_offset = list(map(lambda x_val: x_val + x_axis_offset, x))
# y_offset = list(map(lambda y_val: y_val + y_axis_offset, y))
# Or using numpy to get the same effect
x_normalized = np.array(x) + x_offset
y_normalized = np.array(y) + y_offset

# To create crime rate matrix: Identify the crime coord. to corresponding grids
grid_col = np.array(x_normalized // square_grid_length, dtype=int)
grid_row = np.array(y_normalized // square_grid_length, dtype=int)

# To create crime rate matrix: Calculate matrix size and generate empty matrix
cr_mat_sz = rows * cols
cr_arr = np.zeros(cr_mat_sz, dtype=int)

# Updating crime matrix with number of crimes occurred corresponding to grids
if grid_col.__len__() != grid_row.__len__():
    print("Quit, Something went wrong with the coordinates")
    quit(-1)

for i in range(0, grid_row.__len__()):
    cr_arr[to_index(grid_row[i], grid_col[i], cols)] += 1

print(cr_arr)

# # Visualize updated matrix of crime rates
print("Doesn't match grids")
cr_matrix_flipped = (cr_arr.reshape(rows, cols))
print(cr_matrix_flipped)
print("Matches grids")
cr_matrix = np.flipud(cr_arr.reshape(rows, cols))
print(cr_matrix)

# Test grid counts
# iterate_cr_matrix(cr_matrix, rows, cols)

# Sort crime array for threshold in descending order
cr_arr_sorted = np.sort(cr_arr)[::-1]
print(cr_arr_sorted)

# Calculating crime statistics
median = np.median(cr_arr_sorted)
average = np.average(cr_arr_sorted)
std_dev = np.std(cr_arr_sorted)

print("Median ", median)
print("Average ", average)
print("Standard Deviation ", std_dev)

# Updating blocked and non-blocked areas on matrix
obstacles_arr = cr_arr.copy()

if threshold == 50:
    threshold_val = median
else:
    max_blocked_index = math.floor((rows * cols) * (1 - (threshold / 100)))
    max_blocked_index = 1 if (max_blocked_index <= 0) else max_blocked_index

    threshold_val = cr_arr_sorted[max_blocked_index - 1]

    threshold_val = max(cr_arr_sorted) + 1 if (threshold == 100) else threshold_val

for i in range(0, obstacles_arr.__len__()):
    if obstacles_arr[i] >= threshold_val:
        # Blocked
        obstacles_arr[i] = 0
    else:
        # Open
        obstacles_arr[i] = 1

print(obstacles_arr)

# Draw blocked cells: By looping through crime matrix array and draw squares
for index in range(0, obstacles_arr.__len__()):
    draw_blocked_grid(obstacles_arr[index], index, cols, min(x), min(y), square_grid_length, ax)

# Display plot
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"Crime rate plot : {threshold}% threshold")
# plt.legend()
save_figure(plt, "all_crime_data.png")
plt.show()

# ===== end of program =====
print("=== program terminated ===")
