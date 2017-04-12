#!/usr/bin/env python
import sys
from operator import itemgetter

current_task = None
total_task_count = 0

task_list = []

for line in sys.stdin:
    line = line.strip()
    task, count = line.split("\t", 1)
    try:
        count = int(count)
    except ValueError:
        continue
    
    if current_task == task:
        total_task_count += 1
    else:
        if current_task:
            task_list.append((current_task, total_task_count))
        current_task = task
        total_task_count = 1
        
if current_task == task:
    task_list.append((current_task, total_task_count))
    
task_list = sorted(task_list, key=itemgetter(1), reverse=True)

for x in range(20):
    print("%s\t%s" %(task_list[x][0], task_list[x][1]))
