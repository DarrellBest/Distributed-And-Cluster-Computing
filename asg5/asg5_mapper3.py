#!/usr/bin/env python                                          
import sys                                                                                                
for line in sys.stdin:
    line = line.strip()
    line = line.split(",")
    
    try:
        jobID = line[2]
        taskID = line[3]
    except ValueError:
        continue
    
    print("%s\t%s" %(jobID, taskID))
