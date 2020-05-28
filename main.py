# -------------------------------------------------------
# Assignment 1
# FIXME: Add student id
# Written by Salman Rahman <Student id here don't forget>
# For COMP 472 Section - ABIX – Summer 2020
# --------------------------------------------------------

""" Function Definitions for main driver file """


def sanitize_grid_length(sqr_grid_length):
    sqr_grid_length = sqr_grid_length.replace(",", "")
    sqr_grid_length_exp = Decimal(sqr_grid_length).as_tuple().exponent
    sqr_grid_length_padding = 1 / pow(10, abs(sqr_grid_length_exp) + 2)
    sqr_grid_length = float(sqr_grid_length)

    return sqr_grid_length, sqr_grid_length_padding


if __name__ == "__main__":
    """ Debug variables """
    debug = 1
    test_grid_size = "0.002"
    test_grid_size = "0.010"
    test_threshold = 50

    """ Main Driver file imports """
    import matplotlib.pyplot as plt
    from decimal import Decimal

    from ui import ui
    import data_processing.data as dt
    from path_finding.a_star_algo import aStar
    import data_processing.visualize as visualize

    """ Constant Path Variables """
    shapes_data_path = "data\\Shape\\crime_dt.shp"
    figures_dir_path = "figures\\"

    """ Get grid length and threshold from the user """
    sqr_grid_length = ui.ask_for_grid_length() if debug == 0 else test_grid_size
    sqr_grid_length, sqr_grid_length_padding = sanitize_grid_length(sqr_grid_length)

    threshold = ui.ask_for_threshold() if debug == 0 else test_threshold

    # Fixme: Why is everything blocked for threshold < 50 and 0.001 grids

    """ Logic starts """

    """ Crime data processing and matrices generated for grid plotting & statistics calculation """
    data = dt.data(sqr_grid_length, sqr_grid_length_padding, threshold, shapes_data_path)
    data.update_crime_rate_array()
    data.sort_crime_data_array()
    data.calculate_statistics()
    data.update_obstacles_arr()

    # FIXME: The outputs needs to be cleaned up and easy to read
    """ Print all the generated data and matrices """
    data.print()

    """ Test coordinates for start and destination for debug """
    test_start = (data.lower_x_bound + 1 * 0.002001, data.lower_y_bound + 1 * 0.002001)
    # test_destination = (data.lower_x_bound + 11 * 0.0020001, data.lower_y_bound + 2 * 0.002001)
    # test_destination = (data.lower_x_bound + 18 * 0.0020001, data.lower_y_bound + 6 * 0.002001)
    test_destination = (data.lower_x_bound + 7 * 0.0020001, data.lower_y_bound + 11 * 0.002001)

    # Start x = -73.58983070149999 y = 45.4900685085
    # End x = -73.56 y = 45.50

    """ Get start and destination node coordinates from the user """
    start = ui.ask_for_position(data, "Start") if debug == 0 else test_start
    destination = ui.ask_for_position(data, "Destination") if debug == 0 else test_destination

    """ Generate the path from the start position to the destination position using A* Algorithm """
    aStar = aStar(start, destination, data.obstacles_arr, data)
    path = aStar.run()

    """ Draw data and grids on the figure plot """
    fig1 = plt.figure(figsize=(15, 15))
    ax = fig1.add_subplot(1, 1, 1)

    visualize = visualize.visualize()
    visualize.plot_crime_coordinates(plt, data)
    visualize.draw_initial_grids(data, ax)
    visualize.draw_grid_lines(plt, data)
    visualize.draw_all_blocked_grids(data, ax)
    visualize.draw_path(data, path, ax)
    visualize.save_figure(plt, "all_crime_data.png", figures_dir_path)
    visualize.plot_show(plt, data)

    print("=== program terminated ===")
