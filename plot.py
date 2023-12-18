import matplotlib.pyplot as plt
import numpy as np

def make_partitioned_plot(data: [[[int]]]):
    
    # Data for plotting

    fig, ax = plt.subplots()
    heuristic = ("ff", "nf", "bf", "wf")
    colors = ("b", "g", "r", "m")
    linewidth = 5
    for i in range(4):
        ax.plot([i for i in range(1,21)], data[i][0], linestyle="dotted", linewidth=linewidth, label=heuristic[i] + "/" + "iu", color=colors[i])
        ax.plot([i for i in range(1, 21)], data[i][1], linestyle="solid",  label=heuristic[i] + "/" + "du", color=colors[i])
        linewidth -= 1

    ax.set(xlabel='number of cores', ylabel='success rate',
        title='Partitioners success rates')
    ax.grid()

    plt.legend()
    plt.show()

def make_v_plot(data: [[int]]):
    fig, ax = plt.subplots()
    ax.plot([i for i in range(1, 21)], data[0], label="global scheduling")
    ax.plot([i for i in range(1, 21)], data[1], label="partitioned FFDU")
    ax.plot([i for i in range(1, 21)], data[2], label="edf_k")
    
    ax.set(xlabel='number of cores', ylabel='success rate',
        title='Schedulers success rates')
    ax.grid()

    plt.legend()
    plt.show()