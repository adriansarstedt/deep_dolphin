import numpy as np

from deep_dolphin.helpers.vectors import find_lowest_point
from deep_dolphin.contouring.contour import Contour
from deep_dolphin.helpers.vectors import angle_between_points

from shapely.geometry import Point, LineString, asLineString

class ContourBuilder(object):

    def __init__(self, points=[], existing_contours=[]):

        if len(points) == 0:
            raise ValueError('ContourBuilder cannot be initialised with an empty set of points')
        
        self.unexplored_points = points
        self.initial_point = self.pop_lowest_point()
        self.contour = Contour([self.initial_point])
        self.existing_contours = [
            LineString(contour) for contour in existing_contours
        ]

    def build(self, smoothing_factor):
        while not (self.contour.is_complete() or self.contour.is_empty()):
            next_vertice = self.search_for_next_vertice(smoothing_factor)
            if next_vertice == None:
                self.contour.remove_last_vertice()
            else:
                self.contour.add_vertice(next_vertice)
                self.mark_as_explored(next_vertice)
        
        return ( self.contour.vertices, self.unexplored_points )

    def search_for_next_vertice(self, k):
        k_nearest_neighbours = self.k_nearest_neighbours(k)
        k_nearest_neighbours = self.sort_by_angle_to_contour(k_nearest_neighbours)

        for potential_vertice in k_nearest_neighbours:
            test_contour = self.contour.copy().add_vertice(potential_vertice)

            if test_contour.is_simple() and test_contour.doesnt_intersect(self.existing_contours):
                return( potential_vertice )
    
    def k_nearest_neighbours(self, k):
        neighbours = self.unexplored_points + [self.initial_point]
        neighbours = sorted(neighbours, key=(self.contour.distance_to_point))
        return ( neighbours[:k] )

    def sort_by_angle_to_contour(self, points):
        return ( sorted(points, key=(self.contour.angle_to_point)) )

    def pop_lowest_point(self):
        lowest_point = find_lowest_point(self.unexplored_points)
        self.unexplored_points.remove(lowest_point)
        return ( lowest_point )

    def mark_as_explored(self, point):
        if point in self.unexplored_points:
            self.unexplored_points.remove(point)
