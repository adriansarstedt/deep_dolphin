import numpy as np


class EdgeDetector(object):
    def __init__(self, slice):
        self.slice = np.array(slice)
        self.width, self.height = self.slice.shape

    def get_edge_points(self):
        edge_points = []
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                if self.is_edge_point(x, y):
                    edge_points.append((x, y))
        return edge_points

    def is_edge_point(self, x, y):
        return self.is_not_empty_pixel(x, y) and self.is_neighbouring_empty_pixel(x, y)

    def is_neighbouring_empty_pixel(self, x, y):
        return (
            (self.slice[x + 1][y] < 0.5)
            or (self.slice[x - 1][y] < 0.5)
            or (self.slice[x][y + 1] < 0.5)
            or (self.slice[x][y - 1] < 0.5)
        )

    def is_not_empty_pixel(self, x, y):
        return self.slice[x][y] > 0.5
