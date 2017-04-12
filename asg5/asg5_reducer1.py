#!/usr/bin/env python
import sys

current_jobID = None
total_job_count = 0

for line in sys.stdin:
    jobID = line.strip()
    
    if current_jobID != jobID:
        current_jobID = jobID
        total_job_count = total_job_count + 1
        
print("%s" %total_job_count)