import math

class Job:
    def __init__(self, id, a, b):
        self.id = id
        self.source = a
        self.target = b
        self.targ_distance = self.calculate_distance()
        self.distances = {}
        self.ordered_points = []
        self.status = 0 # 0 - not started; 1 - picked up; 2- dropped


    def calculate_distance(self):
        return math.sqrt((self.source[0] - self.target[0])**2 + (self.source[1] - self.target[1])**2)

    def __repr__(self):
        output = f'Job {self.id}: {self.source} -> {self.target}\n'
        output += f'Distance: {self.targ_distance}\n'
        output += f'Ordered points: {self.ordered_points}\n'
        return output