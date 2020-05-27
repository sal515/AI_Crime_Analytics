# -------------------------------------------------------
# Assignment 1
# FIXME: Add student id
# Written by Salman Rahman <Student id here don't forget>
# For COMP 472 Section - ABIX – Summer 2020
# --------------------------------------------------------

import matplotlib.pyplot as plt
from decimal import Decimal

import data_processing.data as dt
import data_processing.visualize as visualize
from path_finding.a_star_algo import aStar

# ====== user input variables ======
# FIXME : user input
# TODO: grid length should be a string
square_grid_length_input = "0.002"
square_grid_length_input = square_grid_length_input.replace(",", "")
if not square_grid_length_input.replace(".", "").isdigit():
    # wrong input from the user for the grid size
    print("wrong input")
    quit(-1)
square_grid_length_exponent = Decimal(square_grid_length_input).as_tuple().exponent
square_grid_length_padding = 1 / pow(10, abs(square_grid_length_exponent) + 1)
square_grid_length = float(square_grid_length_input)

grid_buffer = square_grid_length * 2
threshold = 90

start = (8, 2)
destination = (6, 8)

# Fixme: Why is everythong blocked for threshold < 50 for 0.001 grids


# ====== constant path variables ======
shapes_data_path = "data\\Shape\\crime_dt.shp"
figures_dir_path = "figures\\"

# ====== logic ======

# Initialize all the data arrays to represent crime matrix
data = dt.data(square_grid_length, square_grid_length_padding, threshold, start, destination, shapes_data_path)
data.update_crime_rate_array()
data.sort_crime_data_arr()
data.calculate_statistics()
data.update_obstacles_arr()

# FIXME
# call astar

aStar = aStar(start, destination, data.obstacles_arr, data)
path = aStar.run()

# call path_to_coordinate_func
import matplotlib.patches as patch

# Print data
# FIXME: The outputs needs to be cleaned up and easy to read
data.print()

# Visualize
fig1 = plt.figure(1)
ax = fig1.add_subplot(1, 1, 1)

visualize = visualize.visualize()
# visualize.plot_crime_coordinates(plt, data)
visualize.draw_initial_patch(plt, ax, data, grid_buffer)
visualize.draw_grids(plt, data)
visualize.draw_all_blocked_grids(data, ax)

# FIXME
# visualize.draw_counts_on_plot(ax, data)
# visualize astar path (ax, data, path)

# ax.add_patch(
#     patch.ConnectionPatch((data.min_x + 0 * data.square_grid_length, data.min_y + data.square_grid_length * 0),
#                           (data.min_x + 5 * data.square_grid_length, data.min_y + data.square_grid_length * 3),
#                           "data", "data", arrowstyle="-|>", shrinkA=1, shrinkB=1,
#                           dpi_cor=30, color="blue", linewidth="2"))
for node in path:
    ax.add_patch(
        patch.ConnectionPatch(data.to_coordinate_from_row_col(node.parent.position),
                              data.to_coordinate_from_row_col(node.position), "data", "data", arrowstyle="-|>",
                              shrinkA=1, shrinkB=1, dpi_cor=30, color="blue", linewidth="2"))

visualize.save_figure(plt, "all_crime_data.png", figures_dir_path)
visualize.plot_show(plt, threshold)

# ===== end of program =====
print("=== program terminated ===")
