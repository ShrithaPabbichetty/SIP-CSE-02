import matplotlib.pyplot as plt
import numpy as np

def plot_results(xpoints, ypoints, xlabel, ylabel):
    
    plt.plot(xpoints, ypoints)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()