from dataclasses import dataclass
from task import Task


@dataclass
class Job:
    task: Task
    deadline: int
    remaining_time: int
    job_id: int
    
    def __init__(self, task: Task, deadline: int, remaining_time: int, job_id: int):
        self.task = task
        self.deadline = deadline
        self.remaining_time = remaining_time
        self.job_id = job_id

    def deadline_missed(self, t: int) -> bool:
        return t > self.deadline and self.remaining_time > 0

    def schedule(self, num_steps: int):
        self.remaining_time -= num_steps

    def is_complete(self) -> bool:
        return self.remaining_time <= 0
    
    def get_task_id(self) -> int:
        return self.task.task_id
