#!/usr/bin/env python
import sys
from operator import itemgetter

current_job = None
total_time_count = 0
job = None

job_list = []
final_list = []

for line in sys.stdin:
    line = line.strip()
    job, time = line.split("\t", 1)
    try:
        time = float(time)
    except ValueError:
        continue
    
    if current_job == job:
        total_time_count += time
    else:
        if current_job:
            job_list.append((current_job, total_time_count))
        current_job = job
        total_time_count = time
        
if current_job == job:
    job_list.append((current_job, total_time_count))
    
for i in range(len(job_list)):
    temp = 300.0 * float(job_list[i][1])
    temp = int(round(temp))
    final_list.append((job_list[i][0], temp))
    
final_list = sorted(final_list, key=itemgetter(1), reverse=True)

for x in range(20):
    print("%s\t%s" %(final_list[x][0], final_list[x][1]))
