import matplotlib.pyplot as plt
import numpy as np

def make_partitioned_scatter_plot(scatter_data: [[[int]]]):
    
    # Data for plotting

    fig, ax = plt.subplots()
    heuristic = ("ff", "nf", "bf", "wf")
    for i in range(4):
        ax.plot([i for i in range(20)], scatter_data[i][0], label=heuristic[i] + "/" + "iu")
        ax.plot([i for i in range(20)], scatter_data[i][1], label=heuristic[i] + "/" + "iu")

    ax.set(xlabel='number of cores', ylabel='success rate',
        title='Partitioners success rates')
    ax.grid()

    plt.show()


