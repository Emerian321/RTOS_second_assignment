import matplotlib.pyplot as plt
import numpy as np


def make_broken_barh(plot_maker: list[list[(int, int)]], output_file: str):
    # Horizontal bar plot
    
    fig, ax = plt.subplots()
    height = 1
    for task in plot_maker:
        ax.broken_barh(task, (height, 1))
        height += 1
    ax.set_ylabel('Task ID')
    ax.set_xlabel('t')
    ax.set_yticks([_+ 1.5 for _ in range(len(plot_maker))], labels=[_ for _ in range(len(plot_maker))])     # Modify y-axis tick labels
    ax.grid(True)                                       # Make grid lines visible
    plt.savefig(output_file)   
    plt.show()

def make_bar_chart(sample_size: int, dm_rates: list[float], edf_rates: list[float], rr_rates: list[float]):
    
    X_axis = np.arange(sample_size)
    width = 0.25
    
    bar1 = plt.bar(X_axis, dm_rates, width, color='r')
    bar2 = plt.bar(X_axis + width, edf_rates, width, color='g')
    bar3 = plt.bar(X_axis + 2 * width, rr_rates, width, color='b')
    
    plt.xlabel('Samples')
    plt.ylabel('Success rate')
    plt.title('Schedulers success rates for constrained tasksets')
    
    plt.xticks(X_axis + width, ['U = ' + str(i*10) + '%' for i in range(4, sample_size+4)])
    plt.legend((bar1[0], bar2[0], bar3[0]), ('Deadline Monotonic', 'Earliest Deadline First', 'Round Robin'))
    plt.show()
    
