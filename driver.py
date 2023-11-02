from utils import euclidean_distance

class Driver:
  def __init__(self, id):
    self.jobs = []
    self.current_location = (0, 0)
    self.total_distance = 0
    self.id = id

  def add_job(self, job):
    self.jobs.append(job)
    self.total_distance += (euclidean_distance(self.current_location, job.start) + job.travel)
    self.current_location = job.end

  def get_total_distance(self):
    return self.total_distance

  def __repr__(self):
    return f'Driver({self.jobs})'
