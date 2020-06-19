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

    def remove_last_vertice(self):
        del(self.vertices[-1])

    def last_vertice(self):
        if len(self.vertices) > 0:
            return self.vertices[-1]
        else:
            return None

    def previous_vertice(self):
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
        return ( len(self.vertices) == 0 )

    def has_not_terminated(self):
        return ( not self.has_terminated() )

    def angle_to_point(self, p):
        return ( -1*angle_between_points(self.previous_vertice(), self.last_vertice(), p) )

    def distance_to_point(self, p):
        if (p == self.last_vertice()):
            return ( 100000000 )
        else:
            return ( distance_between_points(self.last_vertice(), p) )

    def add_vertice(self, point):
        # ensure point is in tuple format
        self.vertices.append(point)
        return ( self )
