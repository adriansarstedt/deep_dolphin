import numpy as np

from deep_dolphin.contouring.contour import Contour
from deep_dolphin.helpers.vectors import angle_between_points

from shapely.geometry import Point, LineString, asLineString

class ContourBuilder(object):

    def __init__(self, points=[], existing_contours=[]):

        if len(points) == 0:
            print("Error!!!")
        
        self.unexplored_points = points
        self.initial_point = self.pop_lowest_point(self.unexplored_points)
        self.contour = Contour([self.initial_point])
        
        self.explored_points = [self.initial_point]
        self.existing_contours = [LineString(contour) for contour in existing_contours]
    
    def __repr__(self):
        return str(self.unexplored_points)

    def __str__(self):
        return str(self.unexplored_points)

    def build_next_contour(self, smoothing_factor):
        while (self.contour.is_incomplete() and self.contour.has_not_terminated()):
            next_vertice = self.search_for_next_vertice(smoothing_factor)
            if next_vertice == None:
                self.contour.remove_last_vertice()
                self.explored_points.append(next_vertice)
            elif next_vertice == self.initial_point:
                self.contour.add_vertice(next_vertice)
                self.explored_points.append(next_vertice)
            else:
                self.unexplored_points.remove(next_vertice)
                self.explored_points.append(next_vertice)
                self.contour.add_vertice(next_vertice)

        print(self.explored_points)
        
        return( self.contour.vertices, self.unexplored_points )

    def search_for_next_vertice(self, smoothing_factor):
        neighbours_sorted_by_distance = sorted(self.unexplored_points + [self.initial_point], key=(self.contour.distance_to_point))
        nearest_neighbours = neighbours_sorted_by_distance[:smoothing_factor]
        nearest_neighbours_sorted_by_angle = sorted(nearest_neighbours, key=(self.contour.angle_to_point))

        for i in range(0, len(nearest_neighbours_sorted_by_angle)):
            potential_next_point = nearest_neighbours_sorted_by_angle[i]
            test_contour = self.contour.copy().add_vertice(potential_next_point)

            if test_contour.has_no_overlaps() and not test_contour.intersects_with(self.existing_contours):
                return( potential_next_point )

    def pop_lowest_point(self, points):
        lowest_point = self.lowest_point(points)
        points.remove(lowest_point)
        return (lowest_point)

    def lowest_point(self, points):
        sorted_points = sorted(points, key=(lambda p: p[1]))
        return ( sorted_points[0] )
