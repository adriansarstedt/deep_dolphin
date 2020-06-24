import numpy as np
from shapely.geometry import Point, Polygon, LineString

from deep_dolphin.helpers.vectors import find_lowest_point
from deep_dolphin.contouring.contour import Contour
from deep_dolphin.helpers.vectors import angle_between_points


class SetToContourConverter(object):
    def __init__(self, points=[], smoothing_factor=3, maximum_side_length=None):
        self.unexplored_points = points
        self.contours = []
        self.smoothing_factor = smoothing_factor
        self.maximum_side_length = maximum_side_length

    def find_all_contours(self):
        while len(self.unexplored_points) > 0:
            next_contour, discarded_points = self.__find_next_contour__()
            if next_contour.is_empty():
                self.unexplored_points += discarded_points[:-1]
            else:
                self.unexplored_points += discarded_points
                self.__remove_unexplored_points_contained_by__(next_contour)
                self.contours.append(next_contour.vertices)

        return self.contours

    # private methods
    def __initialise_new_contour__(self):
        initial_point = self.__pop_lowest_point__()
        return Contour([initial_point])

    def __find_next_contour__(self):
        new_contour = self.__initialise_new_contour__()
        discarded_points = []

        while not (new_contour.is_complete() or new_contour.is_empty()):
            next_vertice = self.__search_for_next_vertice__(
                new_contour, self.smoothing_factor
            )
            if next_vertice == None:
                removed_vertice = new_contour.remove_last_vertice()
                discarded_points.append(removed_vertice)
            else:
                new_contour.add_vertice(next_vertice)
                self.__mark_as_explored__(next_vertice)

        return (new_contour, discarded_points)

    def __search_for_next_vertice__(self, contour, k):
        k_nearest_neighbours = self.__k_nearest_neighbours__(contour, k)
        k_nearest_neighbours = self.__sort_by_angle_to_contour__(
            contour, k_nearest_neighbours
        )

        for potential_vertice in k_nearest_neighbours:
            test_contour = contour.copy().add_vertice(potential_vertice)

            if test_contour.is_simple() and test_contour.doesnt_intersect(
                self.contours
            ):
                return potential_vertice

    def __k_nearest_neighbours__(self, contour, k):
        neighbours = self.unexplored_points.copy()
        if len(contour.vertices) > 3:
            neighbours += [contour.first_vertice()]

        neighbours = sorted(neighbours, key=(contour.distance_to_point))

        if self.maximum_side_length != None:
            neighbours = filter(
                (lambda n: contour.distance_to_point(n) < self.maximum_side_length),
                neighbours,
            )

        return list(neighbours)[:k]

    def __sort_by_angle_to_contour__(self, contour, points):
        return sorted(points, key=(contour.angle_to_point))

    def __pop_lowest_point__(self):
        lowest_point = find_lowest_point(self.unexplored_points)
        self.unexplored_points.remove(lowest_point)
        return lowest_point

    def __mark_as_explored__(self, point):
        if point in self.unexplored_points:
            self.unexplored_points.remove(point)

    def __remove_unexplored_points_contained_by__(self, contour):
        contour_poly = Polygon(contour.vertices)
        enlarged_contour_poly = contour_poly.buffer(2)

        self.unexplored_points = list(
            filter(
                (lambda p: not Point(p).within(enlarged_contour_poly)),
                self.unexplored_points,
            )
        )
