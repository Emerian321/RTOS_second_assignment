import sys
from taskset import TaskSet
from job import Job
from priority_alg import earliest_deadline_first
from heuristics import Heuristic, k_priority, edf_priority

def partitioned_scheduling(taskset: TaskSet, num_cores: int, heuristic: Heuristic, increased_utilisation: bool) -> bool:
    is_schedulable: bool = True
    taskset.sort(increased_utilisation)
    cores = heuristic(taskset.get_tasks(), num_cores)
    for core in cores:
        core.create_task_set()
        
    # begin simulation
    for t in range(feasibility_interval(taskset)):
        print("time ", t, " :")
        for core in cores:
            if not core.schedule(t):
                return not is_schedulable
    return is_schedulable

def golbal_scheduling(taskset: TaskSet, num_cores: int) -> bool:  
    is_schedulable: bool = True
    queue: list[Job] = []
    # Begin simulation
    for t in range(feasibility_interval(taskset)):
        # Release new jobs
        queue += taskset.release_jobs(t)
        # Check for deadlines
        for job in queue:
            if job.deadline_missed(t):
                print(f"Deadline missed for {job} at time {t} !")
                return not is_schedulable
        # assignate to each core the earliest_deadline_job in the queue
        elected_jobs: list[Job] = [None for _ in range(num_cores)]
        for core in range(num_cores):
            # Schedule job
            elected_jobs[core] = earliest_deadline_first(queue)
            if elected_jobs[core] is not None:
                elected_jobs[core].schedule(1)
                queue.remove(elected_jobs[core])
        # check completed jobs
        for job in elected_jobs:
            if not job.is_complete():
                queue.append(job)
    return is_schedulable

def edf_k(taskset: TaskSet, num_cores: int, k: int):
    is_schedulable: bool = True
    taskset.sort(False)
    tasks = taskset.get_tasks()
    cores = k_priority(tasks[:k], num_cores)
    while tasks:
        tasks, elected_task = edf_priority(tasks)
        unfit = True
        core = 0
        while unfit:
            if core >= num_cores:
                # exit code 3
                sys.exit(3)
            unfit = cores[core].is_unfit(elected_task)
            if not unfit:
                cores[core].add_task(elected_task)
            core += 1
    for core in cores:
        core.create_task_set()
        
    # begin simulation
    for t in range(feasibility_interval(taskset)):
        for core in cores:
            if not core.schedule(t):
                return not is_schedulable
    return is_schedulable

def feasibility_interval(taskset: TaskSet) -> int:
    last_deadline = 0
    for task in taskset.get_tasks():
        if last_deadline < task.deadline:
            last_deadline = task.deadline
    return last_deadline