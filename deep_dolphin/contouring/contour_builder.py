import numpy as np
from deep_dolphin.contouring.contour import Contour
from deep_dolphin.helpers.vectors import angle_between_points

class ContourBuilder(object):

    def __init__(self, points=[]):
        self.points = points
        self.contour = Contour([self.initial_point()])

    def __repr__(self):
        return str(self.points)

    def __str__(self):
        return str(self.points)

    def build(self, base_smoothing_factor):
        while (self.contour.is_incomplete() and self.contour.has_not_terminated()):
            next_vertice = self.exhaustive_search_for_next_vertice(base_smoothing_factor)
            self.contour.add_vertice(next_vertice)
        return( self.contour.vertices )

    def exhaustive_search_for_next_vertice(self, base_smoothing_factor):
        for smoothing_factor in range(base_smoothing_factor, len(self.points)):
            if (self.search_for_next_vertice(smoothing_factor) != None):
                return( self.search_for_next_vertice(smoothing_factor) )

    def search_for_next_vertice(self, smoothing_factor):
        neighbours_sorted_by_distance = sorted(self.points, key=(self.contour.distance_to_point))
        nearest_neighbours = neighbours_sorted_by_distance[:smoothing_factor]
        nearest_neighbours_sorted_by_angle = sorted(nearest_neighbours, key=(self.contour.angle_to_point))

        for i in range(0, smoothing_factor):
            potential_next_point = nearest_neighbours_sorted_by_angle[i]
            test_contour = self.contour.copy().add_vertice(potential_next_point)

            if test_contour.is_valid():
                return( potential_next_point )

    def initial_point(self):
        # start contour with lowest point
        sorted_points = sorted(self.points, key=(lambda p: p[1]))
        return( sorted_points[0] )
