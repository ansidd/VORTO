import math
from job import Job

def euclidean_distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def read_data(file):
    

    with open(file, 'r') as f:
        file_content = f.readlines()

    points = []

    for line in file_content[1:]:
        _, a, b = line.split(' ')
        a = a.replace('(', '')
        a = a.replace(')', '')
        a = a.split(',')
        a = (float(a[0]),float(a[1]))
        b = b.replace('(', '')
        b = b.replace(')', '')
        b = b.split(',')
        b = (float(b[0]),float(b[1]))
        points.append((a,b))

    jobs = {}
    new_points = []
    for i, point in enumerate(points):
        jobs[i] = Job(i, point[0], point[1])
        new_points.append([point[0],'source',i])
        new_points.append([point[1],'target',i])

    points = new_points

    distances = {}
    for point in points:
        coords, point_type, job_id = point
        distances[(job_id, point_type)] =  sorted(points, key=lambda x: euclidean_distance(x[0], coords))

    return jobs, points, distances


