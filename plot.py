import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.size": 14,
    "axes.labelsize": 16,
    "axes.titlesize": 16,
    "legend.fontsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
})

_plot_counters = {
    "plot": 0,
    "bar": 0,
}


def _make_filename(prefix, title=None):
    _plot_counters[prefix] += 1
    if title:
        safe_title = title.strip().replace(" ", "_").replace("/", "_")
        return f"{prefix}_{_plot_counters[prefix]}_{safe_title}.pdf"
    return f"{prefix}_{_plot_counters[prefix]}.pdf"


def plot_results(xpoints, y_list, xlabel, ylabel, colors, labels, line_style='-', marker='o', yerr_list=None, filename=None):
    if xpoints and isinstance(xpoints[0], (list, tuple, np.ndarray)):
        x_series = xpoints
    else:
        x_series = [xpoints] * len(y_list)
    for i in range(len(y_list)):
        plt.errorbar(
            x_series[0], y_list[i], yerr=yerr_list[i] if yerr_list is not None else None,
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

    if filename is None:
        filename = _make_filename("plot", ylabel or xlabel)
    plt.savefig(filename, bbox_inches="tight")
    plt.show()


def plot_bar_results(
    labels,
    values,
    xlabel,
    ylabel,
    title="",
    colors=None,
    yerr=None,
    bar_width=0.3,
    filename=None,
):
    plt.figure(figsize=(7.7, 4.8))

    x_positions = np.arange(len(labels))
    bar_width = min(float(bar_width), 0.8)

    plt.bar(
        x_positions,
        values,
        color=colors,
        yerr=yerr,
        width=bar_width,
        capsize=6,
    )

    plt.xticks(x_positions, labels)
    plt.xlim(-0.5, len(labels) - 0.5)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if title:
        plt.title(title)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()

    if filename is None:
        filename = _make_filename("bar", title or ylabel or xlabel)
    plt.savefig(filename, bbox_inches="tight")
    plt.show() 
