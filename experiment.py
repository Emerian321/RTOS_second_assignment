from plot import make_partitioned_plot, make_v_plot
from task_set_generator import generate
from heuristics import first_fit, next_fit, best_fit, worst_fit
from schedulers import partitioned_scheduling, global_scheduling, edf_k

def partitioned_edf_experiment():
    plot = [[[0 for _ in range(20)], [0 for _ in range(20)]] for _ in range(4)]
    heuristics = (first_fit, next_fit, best_fit, worst_fit)
    
    for m in range(20):
        for _ in range(500):
            taskset = generate(4*(m+1), m+1)
            for i in range(4):
                for j in range(2):
                    try:
                        if partitioned_scheduling(taskset, m+1, heuristics[i], j == 0):
                            plot[i][j][m] += 1/500
                    except:
                        pass
    make_partitioned_plot(plot)
    

def global_v_partitioned():
    plot = [[0 for _ in range(20)] for _ in range(3)]
    increasing_utilization = False
    
    for m in range(20):
        for _ in range(500):
            taskset = generate(4*(m+1), m+1)
            try:
                if global_scheduling(taskset, m+1):
                    plot[0][m] += 1/500
            except:
                pass
            try:
                if partitioned_scheduling(taskset, m+1, first_fit, increasing_utilization):
                    plot[1][m] += 1/500
            except:
                pass
            try:
                if edf_k(taskset, m+1, m+1):
                    plot[2][m] += 1/500
            except:
                pass  
    make_v_plot(plot)

partitioned_edf_experiment()

global_v_partitioned()


