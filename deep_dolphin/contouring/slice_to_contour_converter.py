import numpy as np
from shapely.geometry import Point, Polygon

from deep_dolphin.contouring.edge_detector import EdgeDetector
from deep_dolphin.contouring.set_to_contour_converter import SetToContourConverter


class SliceToContourConverter(object):
    def __init__(self, slice, smoothing_factor=3, maximum_side_length=4):
        self.slice = slice
        self.smoothing_factor = smoothing_factor
        self.maximum_side_length = maximum_side_length

    def find_all_contours(self):
        unordered_edge_points = EdgeDetector(self.slice).get_edge_points()
        p_to_c_converter = SetToContourConverter(
            unordered_edge_points, self.smoothing_factor, self.maximum_side_length
        )

        return p_to_c_converter.find_all_contours()
