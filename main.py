import os
import math
from utils import read_data, euclidean_distance
from job import Job
from driver import Driver
import sys


if __name__=="__main__":

    mode = "test"

    #This is for testing on training problems
    if mode=="training":
        files = os.listdir('./Training Problems/')
        files = ['./Training Problems/'+file for file in files]
        costs = []

    else:
        file = sys.argv[1]
        files = [file]


    for file in files:
   
        jobs, points, distances  = read_data(file)

        jobs_done = []
        jobs_remaining = list(jobs.keys())

        drivers = []

        driver_counter = 1;
        drivers = []
        while(len(jobs_remaining)!=0):
            driver = Driver(driver_counter)
            initial_job = sorted(jobs_remaining, key=lambda x: euclidean_distance(jobs[x].start, driver.current_location))[0]
            driver.add_job(jobs[initial_job])
            jobs_remaining.remove(initial_job)
            jobs_done.append(initial_job)
            driver_counter += 1

            while(driver.total_distance<12*60):
                jobs_ordered = sorted([job for job in jobs_remaining if ((driver.total_distance + euclidean_distance(jobs[job].start, driver.current_location) + jobs[job].travel + euclidean_distance(jobs[job].end, (0,0)))<12*60)], key=lambda x: euclidean_distance(jobs[x].start, driver.current_location))
                if len(jobs_ordered)==0:
                    break
                job = jobs_ordered[0]
                
                driver.add_job(jobs[job])
                jobs_remaining.remove(job)
                jobs_done.append(job)

            drivers.append(driver)

    for driver in drivers:
        print([job.id for job in driver.jobs])
            