from dataclasses import dataclass
from task import Task
from job import Job


@dataclass
class TaskSet:
    
    def __init__(self, tasks: list[Task]):
        self.tasks = tasks

    def release_jobs(self, t: int) -> list[Job]:
        jobs: list[Job] = []
        for task in self.tasks:
            if t % task.period == 0:
                jobs.append(task.spawn_job(t))
        return jobs
    
    def next_release(self, t):
        res = [t % self.tasks[i].period for i in range(len(self.tasks)) if t % self.tasks[i].period > 0]
        return min(res) if res else 1
    
    def get_tasks(self)-> list[Task]:
        return self.tasks 

    def __sizeof__(self) -> int:
        return len(self.tasks)
    
    def sort(self, increasing_utilization):
        self.tasks.sort(key=lambda x:x.get_utilization(), reverse=increasing_utilization)
        