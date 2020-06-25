import numpy as np
from shapely.geometry import Point, Polygon

from deep_dolphin.contouring.edge_detector import EdgeDetector
from deep_dolphin.contouring.set_to_contour_converter import SetToContourConverter


class SliceToContourConverter(object):
    def __init__(self, smoothing_factor=3, maximum_side_length=4):
        self.smoothing_factor = smoothing_factor
        self.maximum_side_length = maximum_side_length
        self.set_to_contour_converter = SetToContourConverter(
            self.smoothing_factor, self.maximum_side_length
        )

    def convert(self, slice):
        unordered_edge_points = EdgeDetector(slice).get_edge_points()
        return self.set_to_contour_converter.convert(unordered_edge_points)
