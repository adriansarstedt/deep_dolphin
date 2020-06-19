import numpy as np
from deep_dolphin.contouring.contour import Contour
from deep_dolphin.helpers.vectors import angle_between_points

class ContourBuilder(object):

    def __init__(self, unordered_points_to_build_contour_from=[]):
        self.unexplored_points = unordered_points_to_build_contour_from
        self.explored_points = []
        self.contour = Contour([self.initial_point()])
    
    def __repr__(self):
        return str(self.unexplored_points)

    def __str__(self):
        return str(self.unexplored_points)

    def build(self, smoothing_factor):
        while (self.contour.is_incomplete() and self.contour.has_not_terminated()):
            next_vertice = self.search_for_next_vertice(smoothing_factor)
            if next_vertice == None:
                self.contour.remove_last_vertice()
            else:
                self.unexplored_points.remove(next_vertice)
                self.explored_points.append(next_vertice)
                self.contour.add_vertice(next_vertice)
        
        return( self.contour, self.unexplored_points )

    def search_for_next_vertice(self, smoothing_factor):
        neighbours_sorted_by_distance = sorted(self.unexplored_points, key=(self.contour.distance_to_point))
        nearest_neighbours = neighbours_sorted_by_distance[:smoothing_factor]
        nearest_neighbours_sorted_by_angle = sorted(nearest_neighbours, key=(self.contour.angle_to_point))

        for i in range(0, smoothing_factor):
            potential_next_point = nearest_neighbours_sorted_by_angle[i]
            test_contour = self.contour.copy().add_vertice(potential_next_point)

            if test_contour.has_no_overlaps():
                return( potential_next_point )

    def initial_point(self):
        # start contour with lowest point
        if len(self.unexplored_points) == 0:
            return None
        else:
            sorted_points = sorted(self.unexplored_points, key=(lambda p: p[1]))
            return sorted_points[0]
