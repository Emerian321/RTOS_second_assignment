import sys
from schedulers import *
from heuristics import first_fit, next_fit, best_fit, worst_fit
from task_set_parser import extract_taskset

def main():    
    taskset = extract_taskset(sys.argv[1])
    num_cores = int(sys.argv[2])
    if sys.argv[3] != "-v":
        raise ValueError()
    scheduler = sys.argv[4]
    
    match scheduler:
        case "partitioned":
            
            if sys.argv[5] != "-h":
                raise ValueError()
            heuristic = sys.argv[6]
            match heuristic:
                case "ff":
                    heuristic = first_fit
                case "nf":
                    heuristic = next_fit
                case "bf":
                    heuristic = best_fit
                case "wf":
                    heuristic = worst_fit
                case _:
                    raise ValueError()
            
            if sys.argv[7] != "-s":
                raise ValueError()
            ordering = sys.argv[8] == "iu"
            
            if partitioned_scheduling(taskset, num_cores, heuristic, ordering):
                sys.exit(0)
            else:
                # exit code 2
                print("Not schedulable with simulation.")
                sys.exit(2)
            
        case "global":
            if global_scheduling(taskset, num_cores):
                sys.exit(0)
            else:
                # exit code 2
                print("Not schedulable with simulation.")
                sys.exit(2)
        case _:
            k = int(scheduler)
            if k in range(len(taskset.get_tasks())):
                if edf_k(taskset, num_cores, k):
                    sys.exit(0)
                else:
                    # exit code 2
                    print("Not schedulable with simulation.")
                    sys.exit(2) 
    
main()