# -------------------------------------------------------
# Assignment 1
# FIXME: Add student id
# Written by Salman Rahman <Student id here don't forget>
# For COMP 472 Section - ABIX – Summer 2020
# --------------------------------------------------------

# TODO: Move functions to separate package
# ====== functions ======
import math


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

# ====== user input variables ======
square_grid_length = 0.002
grid_buffer = square_grid_length * 2

# ====== constant path variables ======
shapes_data_path = "data\\Shape\\crime_dt.shp"
figures_dir_path = "figures\\"

# ====== logic ======

# Read shape file using geopanda as a dataframe
crime_data = geopandas.read_file(shapes_data_path)

# Extract all the points from the data frame as a list of points
x_y_pair = list(map(lambda point: list(point.coords)[0], crime_data.geometry))
x = list(map(lambda point: point[0], x_y_pair))
y = list(map(lambda point: point[1], x_y_pair))

# To draw the grid, identifying the bounds of the given data
# By creating a polygon using all the crime data points
poly = polygon(x_y_pair)
bounds = poly.bounds
print("bounds: (minx-0, miny-1, maxx-2, maxy-3) ", bounds)

# To draw the grids on the plot, extracting the x and y points of the grids
cols = int(math.ceil(abs(abs(bounds[2]) - abs(bounds[0])) / square_grid_length))
rows = int(math.ceil(abs(abs(bounds[3]) - abs(bounds[1])) / square_grid_length))

# FIXME: CHECK EQUATION - WHEN TO ADD AND WHEN TO SUBTRACT - DONE?
col_points = list(
    np.arange(bounds[0], (bounds[0] + (cols * square_grid_length) + (square_grid_length / 3)), square_grid_length))

row_points = list(
    np.arange(bounds[1], (bounds[1] + (rows * square_grid_length) + (square_grid_length / 3)), square_grid_length))

print("column points: ", col_points)
print("row points: ", row_points)

# print(f"rows: {rows}, cols: {cols}")
#
# test_bound = bounds[0]
# for i in range(0, rows):
#     if i == 0:
#         print(test_bound)
#         continue
#     test_bound += square_grid_length
#     print(test_bound)

# To draw initial purple patch size,calculate the rectangular grid length & width
# max_y_length = Point(0, bounds[1]).distance(Point(0, bounds[3]))
# max_x_length = Point(bounds[0], 0).distance(Point(bounds[2], 0))
# TODO: The given cordinate is not a perfect square
# max_y_length = abs(abs(bounds[3]) - abs(bounds[1]))
# max_x_length = abs(abs(bounds[2]) - abs(bounds[0]))

max_y_length = abs(abs((bounds[1] + (rows * square_grid_length))) - abs(bounds[1]))
max_x_length = abs(abs((bounds[0] + (cols * square_grid_length))) - abs(bounds[0]))

# For visualization:Create a figure with all the data stored in "figure directory"
# crime_data.geometry.plot(ax=ax)
fig1 = plt.figure(1)
ax = fig1.add_subplot(1, 1, 1)

rect_initial = patches.Rectangle((min(x), min(y)), max_x_length, max_y_length, color="purple")
ax.add_patch(rect_initial)

# Figure axis bounds
plt.axis([(min(x) - grid_buffer), (max(x) + grid_buffer), (min(y) - grid_buffer), (max(y) + grid_buffer)])

# Plot points
plt.plot(x, y, "o")

# Drawing grids
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


# Add rectanges for visualization

rect_high_risk = patches.Rectangle((min(x), min(y)), square_grid_length, square_grid_length, color="red")
ax.add_patch(rect_high_risk)

rect_high_risk = patches.Rectangle((min(x), min(y)), square_grid_length, square_grid_length, color="yellow")
ax.add_patch(rect_high_risk)

# Display plot
save_figure(plt, "all_crime_data.png")
plt.show()

# ===== end of program =====
print("=== program terminated ===")
