import os
import math
from utils import read_data, euclidean_distance
from job import Job
from driver import Driver


if __name__=="__main__":

    mode = "test"

    #This is for testing on training problems
    if mode=="training":
        files = os.listdir('./Training Problems/')
        files = ['./Training Problems/'+file for file in files]
        costs = []

    else:
        file = input()
        files = [file]


    for file in files:
   
        jobs, points, distances  = read_data(file)

        drivers = []

        #ordering jobs in increasing order os distance of pickup point of the corresponding job from the origin
        jobs_in_order = sorted(jobs.keys(), key=lambda x: (math.sqrt(jobs[x].source[0]**2+jobs[x].source[1]**2)))

        jobs_done = []
        jobs_in_progress = []
        
        verbose = False


        #looping until all jobs are completed
        while len(jobs_done)<len(jobs):
            driver = Driver()
            driver.initialize_trip()

            if verbose:
                print("Driver no. ", len(drivers))

            #for each driver looping until the total number of hours worked is less than 12*60
            while(driver.total_distance<12*60):

                #if there are no points queued driver proceeds to unfinished job with nearest point to the origin
                if len(driver.points_to_go_to) == 0:
                    jobs_in_progress.append(jobs_in_order[0])
                    last_point_type, last_point_job_id = driver.add_job(jobs[jobs_in_order[0]])
                    jobs_in_order.remove(jobs_in_order[0])
                
                
                point_queued = driver.points_to_go_to[0]
                recent_job = driver.jobs[-1]

                if verbose:
                    print((last_point_job_id, last_point_type))
                    print("Jobs In Progress: ", jobs_in_progress)
                    print("Jobs Done: ", jobs_done)


                nearest_points = [ i for i in distances[(last_point_job_id, last_point_type)] if i[2] not in jobs_in_progress and i[2] not in jobs_done and i[1]=='source']


                if len(nearest_points) == 0:
                    driver.complete_all_queued_points(jobs, jobs_in_progress, jobs_done, jobs_in_order)
                    break

                nearest_point = nearest_points[0]

                #If reaching the pickup point of nearest unfinished job takes more than 720 mins complete all the drop offs 
                if driver.total_distance + euclidean_distance(nearest_point[0], driver.curr_loc) + driver.distance_left_to_cover >= 12*60:
                    driver.complete_all_queued_points(jobs, jobs_in_progress, jobs_done, jobs_in_order) 
                    break   
                
                #if heading to the next point in queue(dropoff points for previous pickups) is lesser than travelling to nearest pickup point then head to next dropoff point in drivers queue
                elif euclidean_distance(nearest_point[0], driver.curr_loc) >= euclidean_distance(point_queued[0], driver.curr_loc):
                    last_point_type, last_point_job_id = driver.travel_to_next_point_in_queue(jobs)
                    if last_point_type == 'target':
                        jobs_in_progress.remove(last_point_job_id)
                        jobs_done.append(last_point_job_id)
                        if last_point_job_id in jobs_in_order:
                            jobs_in_order.remove(last_point_job_id)

                #if nearest unfinished pickup point is closer than a dropoff point of a job in queue head to the former
                elif nearest_point[1]=='source':
                    if nearest_point[2] in jobs_in_progress or nearest_point[2] in jobs_done:
                        continue
                    else:
                        last_point_type, last_point_job_id = driver.travel_to_new_point(nearest_point, jobs)
                        jobs_in_progress.append(nearest_point[2])
                
            driver.finish_trip()
            drivers.append(driver)

        total_distance = 0
        for driver in drivers:
            if verbose:
                print(driver.total_distance)
            total_distance += driver.total_distance
            print([job.id for job in driver.jobs])

        if mode=="training":
            total_cost = total_distance + (500*len(drivers))
            costs.append(total_cost)

    if verbose:
        print(sum(costs)/len(costs))
            