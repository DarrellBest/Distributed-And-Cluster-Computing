#!/usr/bin/env python
import sys
from operator import itemgetter

current_job = None
high_time = 0
start_time = 0
curr_start_time = 0
stop_time = 0
cur_stop_time = 0
working_list = []
final_list = []

for line in sys.stdin:
    line = line.strip()
    jobID, time, event = line.split("\t")
    
    working_list.append((jobID, time, event))
    
working_list = sorted(working_list, key=itemgetter(0,1))

for i in working_list:
    if i == 0:
        current_job = i[0]
    
    jobID = i[0]
    
    if current_job != jobID:
        high_time = int(stop_time) - int(start_time)
        start_time = i[1]
        stop_time = i[1]
        final_list.append((current_job, high_time, event))
        current_job = i[0]
        
    if int(i[2]) == 1:
        start_time = i[1]
    else:
        stop_time = i[1]
        
    event = i[2] 
    
final_list = sorted(final_list, key=itemgetter(1), reverse=True)

for x in range(20):
    s = ""
        
    if (final_list[x][2] == "2"):
        s = "EVICT"
    elif (final_list[x][2] == "3"):
        s = "FAIL"
    elif (final_list[x][2] == "4"):
        s = "FINISH"
    elif (final_list[x][2] == "5"):
        s = "KILL"
    elif (final_list[x][2] == "6"):
        s = "LOST"
    elif (final_list[x][2] == "7"):
        s = "UPDATE PENDING"
    elif (final_list[x][2] == "8"):
        s = "UPDATE RUNNING"
    elif (final_list[x][2] == "1"):
        s = "SCHEDULE"
    elif (final_list[x][2] == "0"):
        s = "SUBMIT"
    
    print("%s\t%s\t%s" %(final_list[x][0], final_list[x][1], s))