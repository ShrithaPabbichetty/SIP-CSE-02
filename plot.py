import matplotlib.pyplot as plt
import numpy as np


def plot_results(xpoints, y_list, xlabel, ylabel, colors, labels, line_style='-', marker='o'):
    if xpoints and isinstance(xpoints[0], (list, tuple, np.ndarray)):
        x_series = xpoints
    else:
        x_series = [xpoints] * len(y_list)

    for i in range(len(y_list)):
        plt.plot(
            x_series[0],
            y_list[i],
            color=colors[i],
            linestyle=line_style[i] if isinstance(line_style, list) else line_style,
            marker=marker[i] if isinstance(marker, list) else marker,
            label=labels[i]
        )

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()
