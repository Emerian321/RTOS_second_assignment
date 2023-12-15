from taskset import TaskSet
from task import Task
from random import *
from priority_alg import *

class InvalidUtilizationException(Exception):
    pass

def generate(num_tasks: int, sys_utilization: float, num_cores: int) -> TaskSet:
    if sys_utilization < 0 or sys_utilization > num_cores:
        raise InvalidUtilizationException("Utilization must be a float value between 0 and 1")
    offset: int = 0
    MAX_WCET = 100
    total_utilization = 100
    while total_utilization > sys_utilization:
        tasks_set = []
        total_utilization = 0
        
        for task_id in range(num_tasks):
            wcet = uniform(1, MAX_WCET)
            period = uniform(wcet+1, 5*MAX_WCET)
            utilization = wcet / period
            deadline = uniform(0.75 * period, period)  # Randomly generate deadlines within a range
            total_utilization += utilization
            
            task = Task(task_id, int(offset), int(wcet), int(deadline), int(period))
            tasks_set.append(task)

    return TaskSet(tasks_set)

