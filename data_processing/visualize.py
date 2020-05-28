import data_processing.data as dp
import matplotlib.patches as patches


class visualize:

    def __init__(self) -> None:
        # super().__init__()
        pass

    # Plotting the figure
    def plot_show(self, plt, threshold):
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title(f"Crime rate plot : {threshold}% threshold")
        # plt.legend()
        # save_figure(plt, "all_crime_data.png")
        plt.show()

    """ Draw the path from the start postion to the destination position on the grid plot """
    def draw_path(self, data, path, ax, color="limegreen"):
        for v in path:
            start_pos = data.to_coordinate_from_row_col((v.node_a.row, v.node_a.col))
            end_pos = data.to_coordinate_from_row_col((v.node_b.row, v.node_b.col))
            ax.add_patch(patches.ConnectionPatch(start_pos, end_pos, "data", "data", arrowstyle="-", shrinkA=1, shrinkB=1,
                                               dpi_cor=10, color=color, linewidth="8"))

    # To view the crime rates: Draw all the blocked grids as specified color
    def draw_all_blocked_grids(self, data: dp.data, ax, color="yellow"):
        for index in range(0, data.obstacles_arr.__len__()):
            if data.obstacles_arr[index]:
                self.draw_a_grid(index, data, ax, color)

    # # To view crime rate grids: Initially plot all the grids using the safe color
    def draw_initial_grids(self, data: dp.data, ax, color="purple"):
        for index in range(0, data.obstacles_arr.__len__()):
            self.draw_a_grid(index, data, ax, color)

    def draw_a_grid(self, index, data: dp.data, ax, color):

        row_col = data.to_row_col_from_index(index, data.cols)

        grid_loc = (
            data.min_x + row_col[1] * data.square_grid_length, data.min_y + row_col[0] * data.square_grid_length)

        grid = patches.Rectangle(grid_loc, data.square_grid_length, data.square_grid_length, color=color)

        rx, ry = grid.get_xy()
        cx = rx + grid.get_width() / 2.0
        cy = ry + grid.get_height() / 2.0
        # ax.annotate(f"({row_col[0], row_col[1]})", (cx, cy), color='w',  fontsize=8, ha='center',va='center')

        ax.annotate(f"{row_col[0], row_col[1]}", (cx, cy), color='red', weight='bold', fontsize=10, ha='center',
                    va='center')

        ax.add_patch(grid)

    # To view the crime rate data: Plot points
    def plot_crime_coordinates(self, plt, data):
        plt.plot(data.x, data.y, ".")

    # # To view crime rate grids: Initially plot all the grids using the safe color
    # def draw_initial_patch(self, plt, ax, data: dp.data, grid_buffer, color="purple"):
    #     plt.axis(
    #         [(data.min_x - grid_buffer), (data.max_x + grid_buffer), (data.min_y - grid_buffer),
    #          (data.max_y + grid_buffer)])
    #
    #     origin_point = (data.min_x, data.min_y)
    #
    #     rect_initial = patches.Rectangle(origin_point, data.max_x_length, data.max_y_length, color=color)
    #     ax.add_patch(rect_initial)

    # To view the grids: Drawing lines vertical and horizontal
    def draw_grid_lines(self, plt, data):
        for i in data.col_points:
            plt.axvline(x=i)
        for i in data.row_points:
            plt.axhline(y=i)

        # TODO: figure out why lambda doesn't work
        # map(lambda col: plt.axvline(x=col), col_points)

        # FIXME: Fix the grid lines to span only on the data points area
        # start_point = [col_points[3], row_points[0]]
        # end_point = [col_points[3], row_points[(row_points.__len__() - 1)]]
        # plt.plot(start_point, end_point)

    def save_figure(self, plt, figureName, figures_dir_path):
        plt.savefig("".join([figures_dir_path, figureName]))
