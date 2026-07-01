import matplotlib.pyplot as plt
import numpy as np


def plot_results(xpoints, y_list, xlabel, ylabel, colors, line_style=''):
    for i in range(len(y_list)):
        plt.plot(xpoints, y_list[i], color=colors[i], linestyle=line_style, marker='o')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()