from job import Job
from utils import euclidean_distance
import math

class Driver:

  def __init__(self):
    self.jobs = []
    self.total_distance = 0


  def add_job(self, job):
    self.jobs.append(job)
    self.total_distance += math.sqrt((self.curr_loc[0]-job.source[0])**2 + (self.curr_loc[1]-job.source[1])**2)
    self.curr_loc = job.source
    job.status = 1
    self.points_to_go_to.append([job.target,'target',job.id])

    #ordering the queued points in increasing order of distance from current location of the driver
    self.points_to_go_to = sorted(self.points_to_go_to, key=lambda x: euclidean_distance(x[0],self.curr_loc))
    self.distance_left_to_cover = sum([(euclidean_distance(self.points_to_go_to[i][0], self.points_to_go_to[i+1][0])) for i in range(len(self.points_to_go_to)-1)])
    self.distance_left_to_cover += euclidean_distance(self.points_to_go_to[-1][0], (0,0))
    return 'source', job.id

  def initialize_trip(self):
    self.curr_loc = (0,0)
    self.points_to_go_to = []

  def travel_to_next_point_in_queue(self,jobs):
    point = self.points_to_go_to.pop(0)
    self.total_distance += euclidean_distance(self.curr_loc, point[0])
    self.curr_loc = point[0]
    if point[1] == 'target':
      jobs[point[2]].status = 2
      coords, point_type, job_id = point
      #print("Completed Job {}".format(job_id))
      return point_type,job_id 
    elif point[1] == 'source':
      jobs[point[2]].status = 1
      #print(f"Picked up Job {point[2].id}")
      return point_type, job_id


    
  def travel_to_new_point(self, point, jobs):
    
    self.total_distance += euclidean_distance(self.curr_loc, point[0])
    self.curr_loc = point[0]
    if point[1] == 'source':
      jobs[point[2]].status = 1
      point_type, job_id = self.add_job(jobs[point[2]])
      
      #print(f"Picked up Job {point[2]}")
      return point_type, job_id

  def complete_all_queued_points(self, jobs, jobs_in_progress, jobs_done, jobs_in_order):
    while(len(self.points_to_go_to)>0):
      last_point_type, last_point_job_id = self.travel_to_next_point_in_queue(jobs)
      if last_point_type == 'target':
        jobs_in_progress.remove(last_point_job_id)
        jobs_done.append(last_point_job_id)
        if last_point_job_id in jobs_in_order:
          jobs_in_order.remove(last_point_job_id)

  def finish_trip(self):
    self.total_distance+=euclidean_distance((0,0),self.curr_loc)
    self.curr_loc = (0,0)
    
  def __repr__(self):
    output = f'Driver\n'
    output += f'Total distance: {self.total_distance}\n'

