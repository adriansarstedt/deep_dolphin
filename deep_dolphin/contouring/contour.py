import os
from shapely.geometry import Point, LineString, asLineString

from deep_dolphin.helpers.vectors import angle_between_points
from deep_dolphin.helpers.vectors import distance_between_points

class Contour(object):

    def __init__(self, vertices=[]):
        self.vertices = vertices

    ### Vertice functionality

    def first_vertice(self):
        if len(self.vertices) > 0:
            return self.vertices[0]
        else:
            return None

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

    def remove_last_vertice(self):
        last_vertice = self.vertices[-1]
        del(self.vertices[-1])
        return last_vertice

    def add_vertice(self, point):
        self.vertices.append(point)
        return self

    ### Geometry checks

    def is_small(self):
        return (
            (len(self.vertices)<3)
        )

    def is_simple(self):
        return ( 
            self.is_small() or LineString(self.vertices).is_simple
        )

    def intersects(self, contours):
        line_strings = [LineString(contour) for contour in contours]
        for line_string in line_strings:
            if LineString(self.vertices).crosses(line_string):
                return ( True )

    def doesnt_intersect(self, line_strings):
        return (
            not self.intersects(line_strings)
        )

    ### Status checks

    def is_empty(self):
        return ( 
            len(self.vertices)==0 
        )

    def is_complete(self):
        return ( 
            (len(self.vertices)>1) and (self.vertices[0] == self.vertices[-1])
        )

    ## Measurement methods

    def angle_to_point(self, p):
        return ( -1*angle_between_points(self.previous_vertice(), self.last_vertice(), p) )

    def distance_to_point(self, p):
        if (p == self.last_vertice()):
            return ( 100000000 )
        else:
            return ( distance_between_points(self.last_vertice(), p) )

    ### Generic methods

    def __repr__(self):
        return str(self.vertices)

    def __str__(self):
        return str(self.vertices)

    def copy(self):
        return Contour(self.vertices.copy())

    
