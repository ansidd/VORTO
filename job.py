import math

def euclidean_distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


class Job:
  def __init__(self, id, start, end):
    self.id = id
    self.start = start
    self.end = end
    self.status = 0 # 0 - unfinished, 1 - finished
    self.travel = euclidean_distance(start, end)

  def __repr__(self):
    return f'Job({self.id}, {self.start}, {self.end})'

