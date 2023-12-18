from taskset import TaskSet

def feasibility_interval(taskset: TaskSet) -> int:
    last_deadline = 0
    for task in taskset.get_tasks():
        if last_deadline < task.deadline:
            last_deadline = task.deadline
    return last_deadline

def is_taskset_feasible(taskset: TaskSet, num_cores: int):
    tasks = taskset.get_tasks()
    tot_utilization = 0
    for task in tasks:
        if task.get_utilization() > 1:
            print("Not schedulable without simulation")
            exit(3)
        tot_utilization += task.get_utilization()
    if tot_utilization > num_cores:
        print("Not schedulable without simulation")
        exit(3)