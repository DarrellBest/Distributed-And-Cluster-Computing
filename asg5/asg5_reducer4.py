#!/usr/bin/env python
import sys
from operator import itemgetter

current_job = None
total_time_count = 0
job = None

job_list = []

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
    
job_list = sorted(job_list, key=itemgetter(1), reverse=True)

for x in range(20):
    print("%s\t%s" %(job_list[x][0], job_list[x][1]))
