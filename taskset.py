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

    def get_tasks(self)-> list[Task]:
        return self.tasks 

    def __sizeof__(self) -> int:
        return len(self.tasks)
    
    def sort(self, increasing_utilization):
        quicksort(self.tasks, 0, len(self.tasks)-1)
        if not increasing_utilization:
            self.tasks.reverse()
        
def quicksort(array, low, high):
    if low < high:
        
        pi = partition(array, low, high)
        
        quicksort(array, low, pi -1)
        quicksort(array, pi + 1, high)
        

def partition(array: list[Task], low, high):

    # Choose the rightmost element as pivot
    pivot = array[high]

    # Pointer for greater element
    i = low - 1

    # Traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if array[j].get_utilization() <= pivot.get_utilization():

            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1

            # Swapping element at i with element at j
            (array[i], array[j]) = (array[j], array[i])

    # Swap the pivot element with
    # the greater element specified by i
    (array[i + 1], array[high]) = (array[high], array[i + 1])

    # Return the position from where partition is done
    return i + 1