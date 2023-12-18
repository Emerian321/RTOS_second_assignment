from taskset import TaskSet
from job import Job
from task import Task
from priority_alg import earliest_deadline_first
from feasibility import feasibility_interval

class Core:

    task_set = None
    queue = []
    free_utilization = 1
    
    def __init__(self, id: int, tasklist: list[Task]=[]):
        self.id: int = id
        self.tasklist: list[Task] = tasklist
    
    def add_task(self, task: Task):
        self.tasklist.append(task)
        self.free_utilization -= task.get_utilization()
    
    def is_unfit(self, task: Task):
        return self.free_utilization < task.get_utilization()
    
    def update_utilization(self):
        free_space = 1
        for task in self.task_set:
            free_space -= task.get_utilization()
        self.free_utilization = free_space
    
    def create_task_set(self):
        self.task_set = TaskSet(self.tasklist)
        
    def get_free_space(self):
        return self.free_utilization
        
    def schedule(self):
        for time in range(feasibility_interval(self.task_set)):
            
            # Release new jobs
            self.queue += self.task_set.release_jobs(time)
            # Check for deadlines
            for job in self.queue:
                if job.deadline_missed(time):
                    print(f"Deadline missed for {job} at time {time} !")
                    exit(2)
                # Schedule job
                elected_job = earliest_deadline_first(self.queue)
                if elected_job is not None:
                    elected_job.schedule(1)
                    # check completed jobs
                    if elected_job.is_complete():
                        self.queue.remove(elected_job)
        return True
