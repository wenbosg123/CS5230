'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Author: Minh Ho
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
Apr 10th Revision 1:
    Update FCFS implementation, fixed the bug when there are idle time slices between processes
    Thanks Huang Lung-Chen for pointing out
Revision 2:
    Change requirement for future_prediction SRTF => future_prediction shortest job first(SJF), the simpler non-preemptive version.
    Let initial guess = 5 time units.
    Thanks Lee Wei Ping for trying and pointing out the difficulty & ambiguity with future_prediction SRTF.
'''
import sys

input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    completedTime = 0
    
    def __init__(self, id, arrive_time, burst_time): 
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
    
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrive_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    
    current_time = 0
    waiting_time = 0
    
    for process in process_list:

        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        
        schedule.append((current_time,process.id))
        
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    
    average_waiting_time = waiting_time/float(len(process_list))
    
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum ):
    schedule = []

    current_time = 0
    waiting_time = 0

    queue = Queue()
    index = 0
        
    while ((index < len(process_list)) or (not queue.isEmpty())):
        #our round starts
        
        #first of all, let us try to refresh the list
        while (True): 
            # if we have already processed all the items in the list
            if (index >= len(process_list)):
                break

            item = process_list[index]

            # see if we can add the item into the queue, depends on its arrival time
            if (current_time + 4 >= item.arrive_time):
                queue.enqueue(item)
                index = index + 1
            else:
                break    
        

        # alright, now we have done the preparation, to get the babies into the queue.
        # it is time to process them!

        #first of all, let us check if queue is empty or not, if it is empty already, then we just have to wait for another round and add them
        if (not queue.isEmpty()):
            itemToProcess = queue.dequeue()

            schedule.append((current_time, itemToProcess.id))
            # see if we can finish it right away
            if (itemToProcess.burst_time) <= 4:
                itemToProcess.completedTime = current_time + itemToProcess.burst_time
            else:
                itemToProcess.burst_time -= 4
                #put it back
                queue.enqueue(itemToProcess)



        # woohooo, go to next round
        current_time += 4

    for process in process_list:
        waiting_time += process.completedTime - item.arrive_time

    avg_waiting_time = waiting_time/float(len(process_list))

    print(schedule)
    return schedule, avg_waiting_time

def SRTF_scheduling(process_list):
    return (["to be completed, scheduling process_list on SRTF, using process.burst_time to calculate the remaining time of the current process "], 0.0)

def SJF_scheduling(process_list, alpha):
    return (["to be completed, scheduling SJF without using information from process.burst_time"],0.0)


def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])