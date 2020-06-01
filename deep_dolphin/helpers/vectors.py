import numpy as np
from math import sqrt

def angle_between_points(p1, p2, p3):
    # If p1 is not specified set it to be due west
    # Thereby resembling traditional bearing
    if (p1 == None):
        p1 = (p2[0]-1, p2[1])

    return(angle_between_vectors(
        vector_joining_points(p2, p1),
        vector_joining_points(p2, p3)
    ))

def distance_between_points(p1, p2):
    x_displacement = (p1[0] - p2[0]) ** 2
    y_displacement = (p1[1] - p2[1]) ** 2
    return (sqrt(x_displacement+y_displacement))

def angle_between_vectors(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)

    theta = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    theta = np.degrees(theta)

    if (vector_projection(v2, clockwise_normal(v1)) < 0):
        theta = 360 - theta

    return(theta)

def vector_projection(v1, v2):
    return ((np.dot(v1, v2)))

def vector_joining_points(p1, p2):
    return(np.array(p2) - np.array(p1))

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def clockwise_normal(v):
    return((v[1], -v[0]))
