# -------------------------------------------------------
# Assignment 1
# FIXME: Add student id
# Written by Salman Rahman <Student id here don't forget>
# For COMP 472 Section - ABIX – Summer 2020
# --------------------------------------------------------

# TODO: Move functions to separate package
# ====== functions ======
def save_figure(figureName):
    plt.savefig("".join([figures_dir_path, figureName]))


# ====== imports ======
import geopandas
import matplotlib.pyplot as plt
from shapely.geometry import Polygon as polygon
from shapely.geometry import MultiPoint
from shapely.geometry import Point

# ====== user input variables ======
square_grid_length = 0.002

# ====== constant variables ======
shapes_data_path = "data\\Shape\\crime_dt.shp"
figures_dir_path = "figures\\"
# ====== logic ======

# read shape file using geopanda
crime_data = geopandas.read_file(shapes_data_path)

# Create a figure with all the data points in figure directory of the project
crime_data.plot()
save_figure("all_crime_data.png")



# ===== end of program =====
print("program terminated")
