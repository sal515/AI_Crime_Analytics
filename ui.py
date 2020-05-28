from data_processing.data import data as dt


class ui:
    @staticmethod
    def ask_for_grid_length():
        grid_size_str = input("Please provide the numeric value of the preferred grid size: ")

        while not grid_size_str.replace(".", "").replace(",", "").isdigit():
            print(f"Invalid grid size = {grid_size_str} provided")
            grid_size_str = input("Please re-enter the preferred grid size: ")

        return grid_size_str

    @staticmethod
    def ask_for_threshold():
        threshold = input("Please provide the preferred Crime Rate Threshold value as a percentage : ")

        while not (threshold.replace(".", "").replace(",", "").isdigit() and 0 <= float(threshold) <= 100):
            print(f"Invalid Threshold = {threshold} provided")

            threshold = input(f"Please re-enter the threshold between 0 % <= Threshold <= 100 %")

        return float(threshold)

    @staticmethod
    def ask_for_position(data: dt, position_name: str):
        print("")

        x = input(f" {position_name} position : Please provide {data.min_x} <= x <= {data.max_x} coordinate: ")

        while not ui.x_y_sanitization_limits_check(data, x, True):
            print(f"Invalid x = {x} provided")

            x = input(
                f"Please re-enter the x value between {data.min_x} <= x <= {data.max_x}")

        y = input(f"{position_name} position: Please provide {data.min_y} <= y <= {data.max_y} coordinate: ")

        while not ui.x_y_sanitization_limits_check(data, y, False):
            print(f"Invalid y = {y} provided")

            y = input(
                f"Please re-enter the y value between {data.min_y} <= y <= {data.max_y}")

        return tuple([float(x), float(y)])

    @staticmethod
    def x_y_sanitization_limits_check(data, x_or_y, is_x):
        if is_x:
            return x_or_y.replace(".", "").replace(",", "").replace("-",
                                                                    "").isdigit() and data.min_x <= float(x_or_y) <= data.max_x

        return x_or_y.replace(".", "").replace(",", "").replace("-",
                                                                "").isdigit() and data.min_y <= float(x_or_y) <= data.max_y


# TEST CODE
if __name__ == "__main__":
    # ui.ask_for_grid_length()
    """ Get start and destination node coordinates from the user """
    ui.ask_for_threshold()
