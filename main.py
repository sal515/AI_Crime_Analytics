# -------------------------------------------------------
# Assignment 1
# FIXME: Add student id
# Written by Salman Rahman <Student id here don't forget>
# For COMP 472 Section - ABIX – Summer 2020
# --------------------------------------------------------

import matplotlib.pyplot as plt

import data_processing.data as dt
import data_processing.visualize as visualize

# ====== user input variables ======
square_grid_length = 0.002
grid_buffer = square_grid_length * 2
threshold = 90


# ====== constant path variables ======
shapes_data_path = "data\\Shape\\crime_dt.shp"
figures_dir_path = "figures\\"

# ====== logic ======

# Initialize all the data arrays to represent crime matrix
data = dt.data(square_grid_length, threshold, shapes_data_path)
data.update_crime_rate_array()
data.sort_crime_data_arr()
data.calculate_statistics()
data.update_obstacles_arr()

# Print data
# FIXME: The outputs needs to be cleaned up and easy to read
data.print()

# Visualize
fig1 = plt.figure(1)
ax = fig1.add_subplot(1, 1, 1)

visualize = visualize.visualize()
visualize.plot_crime_coordinates(plt, data)
visualize.draw_initial_patch(plt, ax, data, grid_buffer)
visualize.draw_grids(plt, data)
visualize.draw_all_blocked_grids(data, ax)
visualize.save_figure(plt, "all_crime_data.png", figures_dir_path)
visualize.plot_show(plt, threshold)

# ===== end of program =====
print("=== program terminated ===")
