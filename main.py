# -------------------------------------------------------
# Assignment 1
# FIXME: Add student id
# Written by Salman Rahman <Student id here don't forget>
# For COMP 472 Section - ABIX – Summer 2020
# --------------------------------------------------------

""" Main Driver file imports """
import time
import threading
from decimal import Decimal
import matplotlib.pyplot as plt

from ui import ui
import data_processing.data as dt
from path_finding.a_star_algo import aStar
# import data_processing.visualize as visualize
from data_processing.visualize import visualize as visual

rLock = threading.RLock()

""" Function Definitions for main driver file """


def sanitize_grid_length(sqr_grid_length):
    sqr_grid_length = sqr_grid_length.replace(",", "")
    sqr_grid_length_exp = Decimal(sqr_grid_length).as_tuple().exponent
    sqr_grid_length_padding = 1 / pow(10, abs(sqr_grid_length_exp) + 2)
    sqr_grid_length = float(sqr_grid_length)

    return sqr_grid_length, sqr_grid_length_padding


def data_visualization_calculations(visualize: visual, ret: []):
    """ Draw data and grids on the figure plot """
    fig1 = plt.figure(figsize=(15, 15))
    # fig1 = plt.figure(figsize=(25, 25))
    ax = fig1.add_subplot(1, 1, 1)

    visualize.plot_crime_coordinates(plt, data)
    visualize.draw_initial_grids(data, ax)
    visualize.draw_grid_lines(plt, data)
    visualize.draw_all_blocked_grids(data, ax)
    ret.append(fig1)
    ret.append(ax)
    ret.append(visualize)


def timer(delay_duration: int, stop_event: threading.Event, a_star_thread: threading.Thread):
    time.sleep(delay_duration)
    if a_star_thread.is_alive():
        rLock.acquire()
        print(f"Exiting path finding due to timeout of {delay_duration}")
        rLock.release()
        stop_event.set()


def a_star_run_wrapper(aStar: aStar, stop_event: threading.Event, ret: []):
    count = 0
    while not stop_event.is_set() or count != 0:
        count += 1
        p, tc = aStar.run(stop_event)
        ret.append(p)
        ret.append(tc)


if __name__ == "__main__":
    """ Debug variables """
    # FIXME : Set debug to 0 before submission
    debug = 1
    # debug = 0
    # test_grid_size = "0.001"
    test_grid_size = "0.010"
    test_threshold = 50

    # """ Main Driver file imports """
    # import time
    # import threading
    # from decimal import Decimal
    # import matplotlib.pyplot as plt
    #
    # from ui import ui
    # import data_processing.data as dt
    # from path_finding.a_star_algo import aStar
    # import data_processing.visualize as visualize

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

    """ Print all the generated data and matrices """
    data.print()

    """" === START: Path generation calls and data preparation === """

    """ ===== Test coordinates for start and destination for debug ===== """
    # FIXME: Final clear test values
    gridlen = data.sqr_grid_length + data.sqr_grid_length_pad
    # gridlen = data.sqr_grid_length
    test_start = (data.lower_x_bound + 0 * gridlen, data.lower_y_bound + 0 * gridlen)
    # test_start = (data.lower_x_bound + 1 * gridlen, data.lower_y_bound + 2 * gridlen)
    test_destination = (data.lower_x_bound + 0 * gridlen, data.lower_y_bound + 3 * gridlen)
    # test_destination = (data.lower_x_bound + 2 * gridlen, data.lower_y_bound + 0 * gridlen)
    # test_destination = (data.lower_x_bound + 2 * gridlen, data.lower_y_bound + 2 * gridlen)
    # test_destination = (data.lower_x_bound + 1 * gridlen, data.lower_y_bound + 3 * gridlen)
    # test_destination = (data.lower_x_bound + 4 * gridlen, data.lower_y_bound + 4 * gridlen)
    # test_destination = (data.lower_x_bound + 4 * gridlen, data.lower_y_bound + 3 * gridlen)

    if not (data.min_x <= test_destination[0] <= data.max_x + gridlen and data.min_y <= test_destination[
        1] <= data.max_y + gridlen):
        print("Destination is out of bounds")
        quit(-1)

    if not (data.min_x <= test_start[0] <= data.max_x + gridlen and data.min_y <= test_start[
        1] <= data.max_y + gridlen):
        print("Destination is out of bounds")
        quit(-1)

    # Start x = -73.58983070149999 y = 45.4900685085
    # End x = -73.56 y = 45.50
    """ ===== Test coordinates for start and destination for debug ===== """

    """ Get start and destination node coordinates from the user """
    start = ui.ask_for_position(data, "Start") if debug == 0 else test_start
    destination = ui.ask_for_position(data, "Destination") if debug == 0 else test_destination

    """ Generate the path from the start position to the destination position using A* Algorithm """
    aStar = aStar(start, destination, data.obstacles_arr, data)

    # a_star_run_wrapper()

    # FIXME: set timer for the astar run method
    timeout = 10
    aStar_ret = []
    visual_ret = []

    """ Run a_star algorithm for 10 seconds in a thread"""
    a_star_thread_stop = threading.Event()
    a_star_thread = threading.Thread(target=a_star_run_wrapper, args=(aStar, a_star_thread_stop, aStar_ret,))

    """ Timer thread used to time the 10s """
    timer_thread = threading.Thread(target=timer, args=(timeout, a_star_thread_stop, a_star_thread))

    """ Run visualization functions in a thread in parallel to the a_star algorithm """
    visualize = visual()
    visualization_calculation_thread = threading.Thread(target=data_visualization_calculations,
                                                        args=(visualize, visual_ret,))

    """Run all threads"""
    a_star_thread.start()
    timer_thread.start()
    visualization_calculation_thread.start()

    visualization_calculation_thread.join()
    a_star_thread.join()
    timer_thread.join()

    data.total_path_costs = aStar_ret[0]
    path = aStar_ret[1]

    fig1 = visual_ret[0]
    ax = visual_ret[1]
    visualize = visual_ret[2]

    # FIXME CLEAN
    # """Calculating the total heuristic and total actual costs of the path """
    # data.total_path_costs, path = aStar.run()

    print(f"Test output of the threads  cost: {data.total_path_costs}, path: {path}, visualize: {visualize}")
    print("Test path found ", data.path_found)

    # FIXME : Uncomment
    # data.max_of_heuristic_calc = max(aStar.heuristic_estimates_each_vertex) if data.path_found else None
    #
    # print("* Cumulative costs of the path, (f, g, h): ", data.total_path_costs)
    # print("* Heuristic Estimates at each vertex: \n",
    #       aStar.heuristic_estimates_each_vertex[::-1] if data.path_found else None)
    # if data.path_found and data.max_of_heuristic_calc < data.total_path_costs[0]:
    #     print(
    #         f"* The heuristic was admissible, since max of h(v), {data.max_of_heuristic_calc} < c(v), {data.total_path_costs[2]} for every vertex, v")

    """" === END: Path generation calls and data preparation === """

    # """ Draw data and grids on the figure plot """
    # fig1 = plt.figure(figsize=(15, 15))
    # # fig1 = plt.figure(figsize=(25, 25))
    # ax = fig1.add_subplot(1, 1, 1)

    # FIXME: CLEAN after finishing
    # visualize = visualize.visualize()
    # data_visualization_functions()

    if data.path_found:
        visualize.draw_path(data, path, ax)

    visualize.save_figure(plt, "all_crime_data.png", figures_dir_path)
    visualize.plot_show(plt, data)

    print("\n=== program terminated ===")
