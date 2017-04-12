#!/usr/bin/env python
import sys
from operator import itemgetter

current_task = None
current_index = None
task = None

task_list = []

for line in sys.stdin:
    line = line.strip()
    task, index = line.split("\t", 1)
    try:
        index = int(index)
    except ValueError:
        continue
    
    if current_task == task:
        if int(index) > int(current_index):
            current_index = index
    else:
        if current_task:
            task_list.append((current_task, current_index+1))
        current_task = task
        current_index = index
        
if current_task == task:
    task_list.append((current_task, current_index))
    
task_list = sorted(task_list, key=itemgetter(1), reverse=True)

for x in range(20):
    print("%s\t%s" %(task_list[x][0], task_list[x][1]))

