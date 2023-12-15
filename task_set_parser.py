from taskset import TaskSet
from task import Task

def extract_taskset(filename: str) -> TaskSet:
    
    task: list[Task] = []
    file = open(filename, 'r')
    task_id = 0
    for line in file.readlines():
        line = line.split(' ',)
        task.append(Task(task_id, int(line[0]), int(line[1]), int(line[2]), int(line[3])))
        task_id += 1
    file.close()
    return TaskSet(task)