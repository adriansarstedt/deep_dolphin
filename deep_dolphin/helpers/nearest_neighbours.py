from math import sqrt
from deep_dolphin.helpers.sorting import quick_sort

def find_nearest_neighbours(point, neighbours, k):

    def distance(p1, p2):
        x_displacement = (p1[0] - p2[0]) ** 2
        y_displacement = (p1[1] - p2[1]) ** 2
        return (sqrt(x_displacement+y_displacement))

    ordered_neighbours = neighbours.copy()
    if (point in ordered_neighbours):
        ordered_neighbours.remove(point)

    distances = [distance(point, neighbor) for neighbor in ordered_neighbours]

    quick_sort(distances, mirror=ordered_neighbours)
    return(ordered_neighbours[:k])
