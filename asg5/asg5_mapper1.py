#!/usr/bin/env python

import sys

jobArray = []

for job in sys.stdin:
    job = job.strip()
    job = job.split(",")
    try:
        jobID = job[2]
    except ValueError:
        continue
        
    if jobID not in jobArray:
        jobArray.append(jobID)
        print("%s" %jobID)