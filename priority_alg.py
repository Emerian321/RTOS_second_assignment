from typing import Optional
from job import Job

def earliest_deadline_first(jobs: list[Job]) -> Optional[Job]:
    if len(jobs) == 0:
        return None
    elected_job = jobs[0]
    for job in jobs[1:]:
        if job.task.deadline < elected_job.task.deadline:
            elected_job = job
    return elected_job

    
