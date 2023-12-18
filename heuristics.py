from typing import Callable
from core import Core
from task import Task
import sys

Heuristic = Callable[[list[Task], int], list[Core]]

def first_fit(task_list: list[Task], num_cores: int) -> list[Core]:
    # open bins (cores)
    cores = list(create_multiprocessor(num_cores))
    
    # distribute tasks
    for task in task_list:
        
        selected_core = 0
        unfit = True
        while unfit:
            if selected_core >= num_cores:
                # error exit 2
                print("First fit packing impossible")
                sys.exit(2)
            unfit = cores[selected_core].is_unfit(task)
            if not unfit:
                cores[selected_core].add_task(task)
            selected_core += 1
            
    return cores

def next_fit(task_list: list[Task], num_cores: int):
    cores = list(create_multiprocessor(num_cores))   
    
    selected_core = 0
    for task in task_list:
        
        unfit = True
        loopback = 0
        while unfit:
            if loopback >= num_cores:
                # error exit 2
                print("Next fit packing impossible")
                sys.exit(2)
            unfit = cores[selected_core].is_unfit(task)
            if not unfit:
                cores[selected_core].add_task(task)
            else:
                selected_core = (selected_core + 1) % num_cores
            loopback += 1
    
    return cores

def best_fit(task_list: list[Task], num_cores: int):
    cores = list(create_multiprocessor(num_cores))
    
    for task in task_list:
        
        best_selection = None
        best_score = float('inf')
        for core in range(len(cores)):
            if not cores[core].is_unfit(task) and cores[core].get_free_space() < best_score:
                best_score = cores[core].get_free_space()
                best_selection = core
        if best_selection == None:
                # error exit 2
                print("Best fit packing impossible")
                sys.exit(2)
        cores[best_selection].add_task(task)
            
    return cores

def worst_fit(task_list: list[Task], num_cores: int):
    cores = list(create_multiprocessor(num_cores))
    
    for task in task_list:
        
        best_selection = None
        best_score = -float('inf')
        for core in range(len(cores)):
            if not cores[core].is_unfit(task) and cores[core].get_free_space() > best_score:
                best_score = cores[core].get_free_space()
                best_selection = core
        if best_selection == None:
            # error exit 2
            print("Worst fit packing impossible")
            sys.exit(2)
        cores[best_selection].add_task(task)
    return cores

def k_priority(task_list: list[Task], num_cores: int):
    cores = create_multiprocessor(num_cores)   
    
    selected_core = 0
    for task in task_list:
        
        unfit = True
        loopback = 0
        while unfit:
            if loopback >= num_cores:
                # error exit 3
                print("Not schedulable without simulation")
                sys.exit(3)
            unfit = cores[selected_core].is_unfit(task)
            if not unfit:
                cores[selected_core].add_task(task)
            selected_core = (selected_core + 1) % num_cores
            loopback += 1
    
    return cores
    
def edf_priority(tasklist: list[Task]):
    elected_task = tasklist[0]
    for task in tasklist[1:]:
        if task.get_deadline() < elected_task.get_deadline():
            elected_task = task
    tasklist.remove(elected_task)
    return tasklist, elected_task

def create_multiprocessor(num_cores: int) -> list[Core]:
    for core_id in range(num_cores):
        yield Core(core_id)


