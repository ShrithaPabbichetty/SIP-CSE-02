import matplotlib.pyplot as plt
import numpy as np


def plot_results(xpoints, y_list, xlabel, ylabel, colors, labels, line_style='-', marker='o', yerr_list=None):
    if xpoints and isinstance(xpoints[0], (list, tuple, np.ndarray)):
        x_series = xpoints
    else:
        x_series = [xpoints] * len(y_list)

    for i in range(len(y_list)):
        plt.errorbar(
            x_series[0],
            y_list[i],
            yerr=yerr_list[i] if yerr_list is not None else None,
            color=colors[i],
            linestyle=line_style[i] if isinstance(line_style, list) else line_style,
            marker=marker[i] if isinstance(marker, list) else marker,
            label=labels[i],
            capsize=4
        )

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if ylabel == "Speedup vs Baseline":
        plt.axhline(y=1.0, color="black", linestyle="--", linewidth=1)
    plt.legend()
    plt.show()

def plot_bar_results(
    labels,
    values,
    xlabel,
    ylabel,
    title="",
    colors=None,
    yerr=None,
):
    plt.figure(figsize=(7, 5))

    plt.bar(
        labels,
        values,
        color=colors,
        yerr=yerr,
        width=0.3,
        capsize=6,
    )

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if title:
        plt.title(title)

    plt.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()
