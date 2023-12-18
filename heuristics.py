from typing import Callable
from task import Task
from taskset import TaskSet
import sys

Heuristic = Callable[[list[Task], int], list[Task]]

def first_fit(task_list: list[Task], num_cores: int):
    cores = [[] for _ in range(num_cores)]
    utilization = [0 for _ in range(num_cores)]
    # distribute tasks
    for task in task_list:
        
        selected_core = 0
        fit = False
        while not fit:
            if selected_core >= num_cores:
                # error exit 2
                print("First fit packing impossible")
                sys.exit(2)
            task_u = task.get_utilization()
            fit = utilization[selected_core] + task_u <= 1
            if fit:
                cores[selected_core].append(task)
                utilization[selected_core] += task_u
            selected_core += 1
    
    res = []
    for core in cores:
        res.append(TaskSet(core))
    
    return res

def next_fit(task_list: list[Task], num_cores: int):
    cores = [[] for _ in range(num_cores)]  
    utilization = [0 for _ in range(num_cores)]
    
    selected_core = 0
    for task in task_list:
        
        fit = False
        loopback = 0
        while not fit:
            if loopback >= num_cores:
                # error exit 2
                print("Next fit packing impossible")
                sys.exit(2)
            task_u = task.get_utilization()
            fit = utilization[selected_core] + task_u <= 1
            if fit:
                cores[selected_core].append(task)
                utilization[selected_core] += task_u
            else:
                selected_core = (selected_core + 1) % num_cores
            loopback += 1
    
    res = []
    for core in cores:
        res.append(TaskSet(core))
        
    return res

def best_fit(task_list: list[Task], num_cores: int):
    cores = [[] for _ in range(num_cores)]
    utilization = [0 for _ in range(num_cores)]
    
    for task in task_list:
        
        best_selection = None
        best_score = -float('inf')
        for core in range(len(cores)):
            task_u = task.get_utilization()
            fit = utilization[core] + task_u <= 1
            if fit and utilization[core] > best_score:
                best_score = utilization[core]
                best_selection = core
        if best_selection == None:
                # error exit 2
                print("Best fit packing impossible")
                sys.exit(2)
        cores[best_selection].append(task)
        utilization[best_selection] += task.get_utilization()
            
    res = []
    for core in cores:
        res.append(TaskSet(core))
        
    return res

def worst_fit(task_list: list[Task], num_cores: int):
    cores = [[] for _ in range(num_cores)]
    utilization = [0 for _ in range(num_cores)]
    
    for task in task_list:
        
        best_selection = None
        best_score = float('inf')
        for core in range(len(cores)):
            task_u = task.get_utilization()
            fit = utilization[core] + task_u <= 1
            if fit and utilization[core] < best_score:
                best_score = utilization[core]
                best_selection = core
        if best_selection == None:
                # error exit 2
                print("Worst fit packing impossible")
                sys.exit(2)
        cores[best_selection].append(task)
        utilization[best_selection] += task.get_utilization()
            
    res = []
    for core in cores:
        res.append(TaskSet(core))
        
    return res


