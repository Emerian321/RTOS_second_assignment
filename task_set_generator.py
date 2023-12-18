from taskset import TaskSet
from task import Task
from random import *
from priority_alg import *

class InvalidUtilizationException(Exception):
    pass

def generate(num_tasks: int, sys_utilization: float) -> TaskSet:
    if sys_utilization < 0:
        raise InvalidUtilizationException("Utilization must be a float value between 0 and m")
    offset: int = 0
    MAX_WCET = 40
    total_utilization = -float('inf')
    while ((sys_utilization/2) > total_utilization) or (total_utilization > sys_utilization):
        tasks_set = []
        total_utilization = 0
        for task_id in range(num_tasks):
            utilization = float('inf')
            wcet = randint(1, MAX_WCET)
            period = randint(wcet, 5*MAX_WCET)
            utilization = wcet / period
            deadline = period  # implicit deadline
            total_utilization += utilization
            
            task = Task(task_id, int(offset), int(wcet), int(deadline), int(period))
            tasks_set.append(task)

    return TaskSet(tasks_set)
