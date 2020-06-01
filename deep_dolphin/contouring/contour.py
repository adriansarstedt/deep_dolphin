import os
from shapely.geometry import asLineString

class Contour(object):

    def __init__(self, points=[]):
        self.points = points

    def __repr__(self):
        return str(self.points)

    def __str__(self):
        return str(self.points)

    def first_point(self):
        if len(self.points) > 0:
            return self.points[0]
        else:
            return None

    def last_point(self):
        if len(self.points) > 1:
            return self.points[-1]
        else:
            return None

    def previous_point(self):
        if len(self.points) > 1:
            return self.points[-2]
        else:
            return None

    def is_valid(self):
        return( (len(self.points)<2) or (asLineString(self.points).is_simple) )

    def is_complete(self):
        return( (len(self.points)>1) and (self.points[0] == self.points[-1]) )

    def add_point(self, point):
        # ensure point is in tuple format
        new_point = (point[0], point[1])
        self.points.append(new_point)
        return self
