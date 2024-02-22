#data dict
#jobs: (opps, curr_opp, time)
#machines: (job, time)
import time
from operator import itemgetter

import sys


result = []

def init_machine_list(num_machines):
    machine_list = []
    for i in range(0, num_machines):
        machine = []
        machine_list.append([machine, int(0)])

    return machine_list

def lines_to_lists(filename):
    job_list = []
    job_file = open(filename, 'r')
    lines = job_file.readlines()
    for job in lines:
        opp_arr = job.strip('\n').split(" ")
        q = []
        for i in range(0, len(opp_arr), 2):
            q.append([int(opp_arr[i]), int(opp_arr[i+1])])
        job_list.append([q, int(0), int(0)])
    return job_list

def schedule(jobs, machines, num_jobs, num_machines):    
    counter = 0
    while counter < num_jobs:
        for j in range(0, num_jobs):
            print(len(jobs[j][0]))
            if (jobs[j][1] < len(jobs[j][0])):
                cur_opp = jobs[j][1]
                machine_id = jobs[j][0][cur_opp][0]
                machine_time = jobs[j][0][cur_opp][1]
                machines[machine_id][0].append((j, machine_time))
            else:
                print(counter)
                counter = counter + 1
        for m in range(0, num_machines):
            #print(m)
            if machines[m][0]:
                sorted_machine_ops = sorted(machines[m][0], key=itemgetter(1))
                machines[m][0] = sorted_machine_ops
                for i in range(0, len(machines[m][0])):
                    opp = machines[m][0].pop(0)
                    job_id = opp[0] #job_id
                    machine_time = opp[1] #machine_time
                    opp_id = jobs[job_id][1] #operationID (curr opp)
                    comp_job_time = jobs[job_id][2]

                    if machines[m][1] <= comp_job_time:
                        machines[m][1] = comp_job_time               
                    if (opp_id < len(jobs[job_id][0])):
                        jobs[job_id][1] = jobs[job_id][1] + 1 #curr opp iterated
                        comp_job_time = machines[m][1] + machine_time
                        jobs[job_id][2] = comp_job_time
                        machines[m][1] = comp_job_time
                        result.append([job_id, opp_id, machines[m][1]])

    #print(machines)
    #print(len(result))
    return result

print("========================")

start_file = time.time()

jobs = lines_to_lists(sys.argv[1])
metadata = jobs.pop(0)

num_jobs = int(metadata[0][0][0])
num_machines =  int(metadata[0][0][1])
machines = init_machine_list(num_machines)

end_file = time.time()
print(sys.argv[1])
print("Load file time: " + str(end_file-start_file))

start = time.time()
schedule(jobs, machines, num_jobs, num_machines)
end = time.time()
print("Schedule time: " + str(end-start))

print("========================")
