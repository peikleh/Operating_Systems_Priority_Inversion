"""
just run the file as is from the terminal or idle
"""
from __future__ import print_function
import random
ASSIGNEMENT = [[1, 3, 3], [3,2,10], [6,3,3],[8,1,3],[10,2,10], [12,3,3],[26,1,3]]
MY_EXAMPLE = [[1,3,3],[2,2,10],[4,1,3],[10,2,10]]

class priority_inversion():
    def __init__(self, job_list):
        self.LENGTH_TABLE = [3, 10, 3]  # maps job type to job length
        #self.job_q = self.rand_job(10)  # master list of jobs
        self.job_q = job_list

        temp = self.job_q
        temp.sort(key=lambda x: int(x[0]))
        print(temp)

        self.c_job_q = []  # jobs that have arrived and are not finished
        self.t3_started = False  # determines if a job t3 has been started
        self.prev_job = False  # indicates whether the prev_job was finished
        self.prev_ind = 0  # indicates index of previous job
        self.time = 0

    def rand_job(self, length):
        tjq = []
        for i in range(0, length):
            temp = [random.randint(0, 20), random.randint(1, 3)]
            tjq.append([temp[0], temp[1], self.LENGTH_TABLE[temp[1] - 1]])
        temp = tjq
        temp.sort(key=lambda x: int(x[0]))
        print(temp)
        return tjq

    def main_loop(self):
    #Main control loop that increments the timer
        flag = True
        while (flag):

            #add jobs that have arrived to queue
            self.add_c_job_q()
            #if there are jobs in the queue process and run
            if len(self.c_job_q) != 0:
                #choose job with highest priority.
                index = self.choose_job()

                #if job is t3 set t3_started flag
                if (self.c_job_q[index][1] == 3):
                    self.t3_started = True

                #if the previous job was interrupted do this
                if self.prev_job and self.prev_ind != index:
                    #print interrupted job
                    self.print_index(self.prev_ind)
                    #run one timestep of job
                    self.c_job_q[index][2] -= 1
                    #if job is done
                    if self.c_job_q[index][2] == 0:
                        #print job
                        self.print_index(index)
                        #set flag for job in progress to false
                        self.prev_job = False
                        #if job was t3 set its in progress flag to false
                        if self.c_job_q[index][1] == 3:
                            self.t3_started = False
                        #remove job from queue
                        del self.c_job_q[index]
                    #if job is not done
                    else:
                        #set job in progress flag to true and save the index of that job
                        self.prev_job = True
                        self.prev_ind = index
                #if the job was not interrupted
                else:
                    #run one timestep of job
                    self.c_job_q[index][2] -= 1
                    #if job is done
                    if self.c_job_q[index][2] == 0:
                        #print job
                        self.print_index(index)
                        #set job in progress flag to false
                        self.prev_job = False
                        #if job was of type t3 set t3 in progress flag to false
                        if self.c_job_q[index][1] == 3:
                            self.t3_started = False
                        #remove job from queue
                        del self.c_job_q[index]
                    else:
                        self.prev_job = True
                        self.prev_ind = index
            #if all jobs done end
            if(self.is_done()):
                flag = False
            self.time += 1

    def print_index(self, index):
        #prints a job
        if self.c_job_q[index][1] == 1:
            print('time ' + str(self.time) + ', t1{', end="")
            for i in range(0, 3 - self.c_job_q[index][2]):
                print('1', end="")
            print('}t1')
        elif self.c_job_q[index][1] == 2:
            print('time ' + str(self.time) + ', t2{', end="")
            for i in range(0, 10 - self.c_job_q[index][2]):
                print('N', end="")
            print('}t2')
        else:
            print('time ' + str(self.time) + ', t3{', end="")
            for i in range(0, 3 - self.c_job_q[index][2]):
                print('3', end="")
            print('}t3')

    def add_c_job_q(self):
        for jobs in self.job_q:
            if (jobs[0] == self.time):
                self.c_job_q.append(jobs)

    def choose_job(self):
        #this is where priority inversion is corrected

        #if a t3 is in progress
        if self.t3_started:
            #if the queue has a job of t1
            if self.contains_t1():

                #keep running t3
                for i in range(0, len(self.c_job_q)):
                    if (self.c_job_q[i][1] == 3):
                        return i
            #choose according to normal priority
            else:
                choice = [0, self.c_job_q[0][1]]
                for i in range(0, len(self.c_job_q)):
                    if self.c_job_q[i][1] < choice[1]:
                        choice = [i, self.c_job_q[i][1]]
                return choice[0]
        #choose according to normal priority
        else:
            choice = [0, self.c_job_q[0][1]]
            for i in range(0, len(self.c_job_q)):
                if self.c_job_q[i][1] < choice[1]:
                    choice = [i, self.c_job_q[i][1]]
            return choice[0]

    def contains_t1(self):
        for lists in self.c_job_q:
            if lists[1] == 1:
                return True
        return False

    def is_done(self):
        if len(self.c_job_q) == 0:
            for lists in self.job_q:
                if lists[0] > self.time:
                    return False
            return True
        else:
            return False


def main():
    print("\n\nThe following output is slightly different from the output example provided\n in the assignment. The time stamp represents job end times rather than start times.")
    print("The priority inversion is still clearly evident in the output")
    print("_______________________________________________________________________\n\n")
    print("Results from a priority inversion ")
    x = priority_inversion(MY_EXAMPLE)

    x.main_loop()
    print("\nResults from provided dataset")
    y = priority_inversion(ASSIGNEMENT)
    y.main_loop()

main()
