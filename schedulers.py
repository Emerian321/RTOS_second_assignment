import sys
from taskset import TaskSet
from job import Job
from priority_alg import earliest_deadline_first
from heuristics import Heuristic
from feasibility import feasibility_interval

def partitioned_scheduling(taskset: TaskSet, num_cores: int, heuristic: Heuristic, increasing_utilisation: bool) -> bool:
    is_schedulable: bool = True
    taskset.sort(increasing_utilisation)
    partition = heuristic(taskset.get_tasks(), num_cores)
    cores = [[] for _ in range(num_cores)]
    # Begin simulation
    for t in range(feasibility_interval(taskset)):
        for core in range(num_cores):
            # Release new jobs
            cores[core] += partition[core].release_jobs(t)
            # Check for deadlines
            for job in cores[core]:
                if job.deadline_missed(t):
                    print(f"Deadline missed for {job} at time {t} !")
                    # exit code 2
                    sys.exit(2)
                
            elected_job = earliest_deadline_first(cores[core])
            if elected_job is not None:
                elected_job.schedule(1)
                # check completed job
                if elected_job.is_complete():
                    cores[core].remove(elected_job)
      
    return is_schedulable

def global_scheduling(taskset: TaskSet, num_cores: int) -> bool:  
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
                # exit code 2
                sys.exit(2)
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
            if job and not job.is_complete():
                queue.append(job)
    return is_schedulable

def edf_k(taskset: TaskSet, num_cores: int, k: int):
    
    ABSOLUTE_TASKS, EDF_TASKS = "1", "2" 
    
    increasing_utilization = False
    partition = [{ABSOLUTE_TASKS: [], EDF_TASKS: []} for _ in range(num_cores)]
    utilization = [0 for _ in range(num_cores)]
    taskset.sort(increasing_utilization)
    tasks = taskset.get_tasks()
    
    # schedule absolute tasks
    
    selected_core = 0
    for task in tasks[:k-1]:
        
        fit = False
        loopback = 0
        while not fit:
            if loopback >= num_cores:
                # error exit 2
                print("Worst fit packing impossible")
                sys.exit(2)
            fit = utilization[selected_core] + task.get_utilization() <= 1
            if fit:
                partition[selected_core][ABSOLUTE_TASKS].append(task)
                utilization[selected_core] += task.get_utilization()
            else:
                selected_core = (selected_core + 1) % num_cores
            loopback += 1
        
    # schedule EDF Tasks
    
    edf_tasks = tasks[k-1:]
    while edf_tasks:
        
        for core in range(num_cores):
            if edf_tasks:
                elected_task = min(edf_tasks, key= lambda task: task.get_deadline())
                
                partition[core][EDF_TASKS].append(elected_task)
                edf_tasks.remove(elected_task)
    
    # convert into Tasksets
    for core in range(num_cores):
        partition[core][ABSOLUTE_TASKS] = TaskSet(partition[core][ABSOLUTE_TASKS])
        partition[core][EDF_TASKS] = TaskSet(partition[core][EDF_TASKS])
    
    core_queues = [{ABSOLUTE_TASKS: [], EDF_TASKS: []} for _ in range(num_cores)]
    
    # schedule
    is_schedulable = True
    for t in range(feasibility_interval(taskset)):
        for core in range(num_cores):
            # Release new jobs
            core_queues[core][ABSOLUTE_TASKS] += partition[core][ABSOLUTE_TASKS].release_jobs(t)
            core_queues[core][EDF_TASKS] += partition[core][EDF_TASKS].release_jobs(t)
            # Check for deadlines
            for job in core_queues[core][ABSOLUTE_TASKS]:
                if job.deadline_missed(t):
                    print(f"Deadline missed for {job} at time {t} !")
                    # exit code 2
                    sys.exit(2)
            for job in core_queues[core][EDF_TASKS]:
                if job.deadline_missed(t):
                    print(f"Deadline missed for {job} at time {t} !")
                    # exit code 2
                    sys.exit(2)
            
            if core_queues[core][ABSOLUTE_TASKS]:
                elected_job = core_queues[core][ABSOLUTE_TASKS][0]
                elected_job.schedule(1)
                if elected_job.is_complete():
                    core_queues[core][ABSOLUTE_TASKS].remove(elected_job)
            else:
                elected_job = earliest_deadline_first(core_queues[core][EDF_TASKS])
                if elected_job is not None:
                    elected_job.schedule(1)
                    # check completed job
                    if elected_job.is_complete():
                        core_queues[core][EDF_TASKS].remove(elected_job)
    return is_schedulable
    