#!/usr/bin/env python

import sys

for job in sys.stdin:
    job = job.strip()
    job = job.split(",")
    try:
        jobID = job[2]
        time = job[0]
        event = job[3]
    except ValueError:
        continue
        
    print("%s\t%s\t%s" %(jobID, time, event))