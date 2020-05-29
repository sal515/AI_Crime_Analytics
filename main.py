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
    # FIXME : Set debug to 0 before submission
    # debug = 1
    debug = 0
    test_grid_size = "0.002"
    # test_grid_size = "0.010"
    test_threshold = 50

    """ Main Driver file imports """
    import matplotlib.pyplot as plt
    from decimal import Decimal

    from ui import ui
    import data_processing.data as dt
    from path_finding.a_star_algo import aStar as a_star
    from  data_processing.visualize import visualize as visual

    """ Constant Path Variables """
    shapes_data_path = "data\\Shape\\crime_dt.shp"
    figures_dir_path = "figures\\"

    once = True

    while True:

        if not once:
            choice = input("\n\nDo you want to continue? y/n ")
            if choice.isalpha() and (choice == "n" or choice == "N"):
                break
        once = False

        """ Get grid length and threshold from the user """
        sqr_grid_length = ui.ask_for_grid_length() if debug == 0 else test_grid_size
        sqr_grid_length, sqr_grid_length_padding = sanitize_grid_length(sqr_grid_length)

        threshold = ui.ask_for_threshold() if debug == 0 else test_threshold

        """ Logic starts """

        """ Crime data processing and matrices generated for grid plotting & statistics calculation """
        data = dt.data(sqr_grid_length, sqr_grid_length_padding, threshold, shapes_data_path)
        data.update_crime_rate_array()
        data.sort_crime_data_array()
        data.calculate_statistics()
        data.update_obstacles_arr()

        """ Print all the generated data and matrices """
        data.print()


        """" === START: Path generation calls and data preparation === """

        """ Get start and destination node coordinates from the user """
        start = ui.ask_for_position(data, "Start") if debug == 0 else test_start
        destination = ui.ask_for_position(data, "Destination") if debug == 0 else test_destination

        """ Generate the path from the start position to the destination position using A* Algorithm """
        aStar = a_star(start, destination, data.obstacles_arr, data)

        """Calculating the total heuristic and total actual costs of the path """
        timeout = 10
        data.total_path_costs, path = aStar.run(data, timeout)
        print(f"* Path search took: {round(data.time_taken, 4)}s")

        if data.total_path_costs is not None and len(path) > 0:

            data.max_of_heuristic_calc = max(aStar.heuristic_estimates_each_vertex) if data.path_found else None

            print("* Cumulative costs of the path, (f, g, h): ", data.total_path_costs)
            print("* Heuristic Estimates at each vertex: \n",
                  aStar.heuristic_estimates_each_vertex[::-1] if data.path_found else None)
            if data.path_found and data.max_of_heuristic_calc < data.total_path_costs[0]:
                print(
                    f"* The heuristic was admissible, since max of h(v), {data.max_of_heuristic_calc} < c(v), {data.total_path_costs[2]} for every vertex, v")

        """" === END: Path generation calls and data preparation === """

        print("\n* Please wait, Generating the plot...")
        print(" * Note: for smaller grids plotting takes quite some time\n")

        """ Draw data and grids on the figure plot """
        fig1 = plt.figure(figsize=(15, 15))
        # fig1 = plt.figure(figsize=(25, 25))
        ax = fig1.add_subplot(1, 1, 1)

        visualize = visual()
        # visualize.plot_crime_coordinates(plt, data)

        grid_buffer = data.sqr_grid_length * 0.5
        visualize.draw_initial_patch(plt, ax, data, grid_buffer)

        visualize.draw_grid_lines(plt, data)
        visualize.draw_all_blocked_grids(data, ax)
        if data.path_found:
            visualize.draw_path(data, path, ax)
        visualize.save_figure(plt, "all_crime_data.png", figures_dir_path)
        visualize.plot_show(plt, data)
        print("\n* Plot generation complete")

    print("\n*** Program terminated *** ===")
