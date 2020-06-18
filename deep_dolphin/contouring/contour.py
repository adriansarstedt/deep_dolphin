import os
from shapely.geometry import asLineString
from deep_dolphin.helpers.vectors import angle_between_points
from deep_dolphin.helpers.vectors import distance_between_points

class Contour(object):

    def __init__(self, vertices=[]):
        self.vertices = vertices

    def __repr__(self):
        return str(self.vertices)

    def __str__(self):
        return str(self.vertices)

    def copy(self):
        return Contour(self.vertices.copy())

    def first_point(self):
        if len(self.vertices) > 0:
            return self.vertices[0]
        else:
            return None

    def last_point(self):
        if len(self.vertices) > 0:
            return self.vertices[-1]
        else:
            return None

    def previous_point(self):
        if len(self.vertices) > 1:
            return self.vertices[-2]
        else:
            return None

    def is_valid(self):
        return (
            (len(self.vertices)>2)
        )

    def has_no_overlaps(self):
        return ( (len(self.vertices)<2) or (asLineString(self.vertices).is_simple) )

    def is_complete(self):
        return ( (len(self.vertices)>1) and (self.vertices[0] == self.vertices[-1]) )

    def is_incomplete(self):
        return( not self.is_complete() )

    def has_terminated(self):
        return ( self.vertices[-1] == None )

    def has_not_terminated(self):
        return ( not self.has_terminated() )

    def angle_to_point(self, p):
        return ( -1*angle_between_points(self.previous_point(), self.last_point(), p) )

    def distance_to_point(self, p):
        if (p == self.last_point()):
            return ( 100000000 )
        else:
            return ( distance_between_points(self.last_point(), p) )

    def add_vertice(self, point):
        # ensure point is in tuple format
        if point == None:
            self.vertices.append(self.vertices[0])
        else:
            new_point = (point[0], point[1])
            self.vertices.append(new_point)
        return self
