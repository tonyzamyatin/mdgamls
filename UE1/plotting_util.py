from typing import Tuple

from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from xarray import DataArray


def line_plot_with_marks(data_array: DataArray, x_coord: str, label: str = None,
                         line_color: str = 'teal', mark_color: str = 'grey',
                         linestyle: str = '-', linewidth: float = 1.5,
                         marker: str = 'o', markersize: float = 20, display=True) -> None:
    """
    Creates a line plot with the individual datapoints marked by dots.
    :param data_array: The data array
    :param x_coord: The coordinate of the data array to use as the x-axis in the plot
    :param label: Optional label for the line plot
    :param line_color: Optional color for the line plot
    :param mark_color: Optional color for the marker points
    :param linestyle: Optional linestyle for the line plot (e.g., '-', '--', '-.')
    :param linewidth: Optional thickness of the line
    :param marker: Optional marker style for the scatter points (e.g., 'o', 'x', '^')
    :param markersize: Optional size of the scatter points
    :param display: Whether to display the plot
    """
    data_array.plot.line(x=x_coord, color=line_color, linestyle=linestyle, label=label, linewidth=linewidth, add_legend=label is not None)
    data_array.plot.scatter(x=x_coord, color=mark_color, marker=marker, s=markersize, add_legend=False)
    if display:
        plt.show()


def scatter_plot_with_statistics(data_array: DataArray, x_coord: str, location: Tuple[str, float], scale: Tuple[str, float], display=True) -> None:
    """
    Creates a scatter plot for the given data array.
    :param data_array: The data array
    :param x_coord: The coordinate of the data array to use as the x-axis in the plot
    :param location: The location parameter to be plotted and its name
    :param scale: The scale parameter to be plotted and its name
    :param display: Whether to display the plot
    """
    data_array.plot.scatter(x=x_coord, marker='x')
    plt.axhline(location[1], color='red', linestyle='--', label=location[0].capitalize())
    plt.axhline(location[1] + scale[1], color='grey', linestyle='--')
    plt.axhline(location[1] - scale[1], color='grey', linestyle='--')

    # Custom legend entry for ±1 Std Dev
    legend_line = Line2D([0], [0], color='grey', linestyle='--', label=f'±1 {scale[0].capitalize()}')
    # Manually create the legend with both the custom entry and the Median Slope entry
    plt.legend(handles=[legend_line, Line2D([0], [0], color='red', linestyle='--', label=location[0].capitalize())])
    if display:
        plt.show()
