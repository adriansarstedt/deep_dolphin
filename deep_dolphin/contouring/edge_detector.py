import numpy as np

class EdgeDetector(object):

    def __init__(self, slice):
        self.slice = slice

    def get_edge_points(self):
        edge_points = []
        for x in range(1, len(self.slice)-1):
            for y in range(1, len(self.slice[0])-1):
                if self.is_non_zero(x, y, self.slice) and self.is_edge_point(x, y, self.slice):
                    edge_points.append((x, y))
        return( edge_points )

    def is_edge_point(self, x, y, mask):
        return (
            (mask[x+1][y] < 0.5) or
            (mask[x-1][y] < 0.5) or
            (mask[x][y+1] < 0.5) or
            (mask[x][y-1] < 0.5)
        )

    def is_non_zero(self, x, y, mask):
        return (
            mask[x][y] > 0.5
        )