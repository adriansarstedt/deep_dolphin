import numpy as np

from deep_dolphin.helpers.vectors import find_lowest_point
from deep_dolphin.contouring.contour import Contour
from deep_dolphin.helpers.vectors import angle_between_points

from shapely.geometry import Point, Polygon, LineString

class SetToContourConverter(object):

    def __init__(self, points=[], smoothing_factor=3):
        self.unexplored_points = points
        self.contours = []
        self.smoothing_factor = smoothing_factor

    def find_all_contours(self):
        while len(self.unexplored_points) > 0:
            next_contour = self.__find_next_contour()
            self.__remove_unexplored_points_contained_by(next_contour)
            if not next_contour.is_empty():
                self.contours.append(next_contour.vertices)

        return self.contours

    # private methods
    def __initialise_new_contour(self):
        initial_point = self.__pop_lowest_point()
        return Contour([initial_point])

    def __find_next_contour(self):
        new_contour = self.__initialise_new_contour()

        while not (new_contour.is_complete() or new_contour.is_empty()):
            next_vertice = self.__search_for_next_vertice(new_contour, self.smoothing_factor)
            if next_vertice == None:
                new_contour.remove_last_vertice()
            else:
                new_contour.add_vertice(next_vertice)
                self.__mark_as_explored(next_vertice)

        return new_contour

    def __search_for_next_vertice(self, contour, k):
        k_nearest_neighbours = self.__k_nearest_neighbours(contour, k)
        k_nearest_neighbours = self.__sort_by_angle_to_contour(contour, k_nearest_neighbours)

        for potential_vertice in k_nearest_neighbours:
            test_contour = contour.copy().add_vertice(potential_vertice)

            if test_contour.is_simple() and test_contour.doesnt_intersect(self.contours):
                return( potential_vertice )
    
    def __k_nearest_neighbours(self, contour, k):
        neighbours = self.unexplored_points.copy()
        if len(contour.vertices) > 2:
            neighbours += [contour.first_vertice()]

        neighbours = sorted(neighbours, key=(contour.distance_to_point))
        return ( neighbours[:k] )

    def __sort_by_angle_to_contour(self, contour, points):
        return ( sorted(points, key=(contour.angle_to_point)) )    

    def __pop_lowest_point(self):
        lowest_point = find_lowest_point(self.unexplored_points)
        self.unexplored_points.remove(lowest_point)
        return ( lowest_point )

    def __mark_as_explored(self, point):
        if point in self.unexplored_points:
            self.unexplored_points.remove(point)

    def __remove_unexplored_points_contained_by(self, contour):
        contour_poly = Polygon(contour.vertices)
        enlarged_contour_poly = contour_poly.buffer(2)

        self.unexplored_points = list(filter(
            (lambda p: not Point(p).within(enlarged_contour_poly)), self.unexplored_points
        ))
