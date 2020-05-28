import data_processing.data as dp
import matplotlib.patches as patches


class visualize:

    def __init__(self) -> None:
        pass

    @staticmethod
    def plot_show(plt, data) -> None:
        """ Plotting the figure
        :param plt:
        :param data:
        """
        plt.xlabel("""Longitude
        x-axis / columns """)
        plt.ylabel("""Latitude
        y-axis / rows """)
        plt.title(f"""Crime rate plot : {data.threshold}% threshold
        grid_size = {data.sqr_grid_length}, threshold_value= {round(data.threshold_val, 2)} 
        median = {round(data.median, 2)}, std_dev={round(data.std_dev, 2)}, avg={round(data.average, 2)},
        actual_costs of (f,g,h)={data.total_path_costs if data.path_found else "-"}
        max_heuristic_calculated={data.max_of_heuristic_calc if data.path_found else "-"}
        """)
        plt.show()

    @staticmethod
    def draw_path(data, path, ax, color: str = "limegreen") -> None:
        """ Draw the path from the start position to the destination position on the grid plot
        :param data:
        :param path:
        :param ax:
        :param color:
        """
        for v in path:
            start_pos = data.to_coordinate_from_row_col((v.node_a.row, v.node_a.col))
            end_pos = data.to_coordinate_from_row_col((v.node_b.row, v.node_b.col))
            ax.add_patch(
                patches.ConnectionPatch(start_pos, end_pos, "data", "data", arrowstyle="-", shrinkA=1, shrinkB=1,
                                        dpi_cor=10, color=color, linewidth="8"))

    def draw_all_blocked_grids(self, data: dp.data, ax, color="yellow", annotate_row_col=False):
        """ To view the crime rates: Draw all the blocked grids as specified color
        :param data:
        :param ax:
        :param color:
        :param annotate_row_col:
        """
        for index in range(0, data.obstacles_arr.__len__()):
            if data.obstacles_arr[index]:
                self.draw_a_grid(index, data, ax, color, annotate_row_col)

    def draw_initial_grids(self, data: dp.data, ax, color="purple", annotate_row_col=False):
        """ To view crime rate grids: Initially plot all the grids using the safe color """
        for index in range(0, data.obstacles_arr.__len__()):
            self.draw_a_grid(index, data, ax, color, annotate_row_col)

    @staticmethod
    def draw_a_grid(index, data: dp.data, ax, color: str, annotate_row_col: bool):
        """ Draw a grid by itself - it could be a blocked or non-blocked grid based on provided inputs """
        row_col = data.to_row_col_from_index(index, data.cols)
        grid_loc = (
            data.min_x + row_col[1] * data.sqr_grid_length, data.min_y + row_col[0] * data.sqr_grid_length)
        grid = patches.Rectangle(grid_loc, data.sqr_grid_length, data.sqr_grid_length, color=color)

        rx, ry = grid.get_xy()
        cx = rx + grid.get_width() / 2.0
        cy = ry + grid.get_height() / 2.0

        if annotate_row_col:
            # Annotating the row and col on the grids for easier debugging
            ax.annotate(f"{row_col[0], row_col[1]}", (cx, cy), color='red', weight='bold', fontsize=10, ha='center',
                        va='center')

        else:
            display_str = f"""{data.crime_rate_arr[index]}
{row_col[0], row_col[1]}"""
            ax.annotate(display_str, (cx, cy), color='red', weight='bold', fontsize=10, ha='center',
                        va='center')

        ax.add_patch(grid)

    @staticmethod
    def plot_crime_coordinates(plt, data):
        """ To see the data points from the shapate file - Plots all the data points on the plot """
        plt.plot(data.x, data.y, ".")

    @staticmethod
    def draw_grid_lines(plt, data):
        """ Draw the grid lines on the plot to visualize the grids """
        for i in data.col_points:
            plt.axvline(x=i)
        for i in data.row_points:
            plt.axhline(y=i)

    @staticmethod
    def save_figure(plt, figureName, figures_dir_path):
        """ store the figure in the given dir path and use the filename with extension provided as func input"""
        plt.savefig("".join([figures_dir_path, figureName]))
