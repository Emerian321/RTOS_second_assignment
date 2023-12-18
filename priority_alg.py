from typing import Optional
from job import Job

def earliest_deadline_first(jobs: list[Job]) -> Optional[Job]:
    if not jobs:
        return None
    return min(jobs, key=lambda job: job.deadline)

    
