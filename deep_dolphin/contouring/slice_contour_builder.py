import numpy as np
from shapely.geometry import Point, Polygon

from deep_dolphin.contouring.edge_detector import EdgeDetector
from deep_dolphin.contouring.contour_builder import ContourBuilder

class SliceContourBuilder(object):

    def __init__(self, slice, smoothing_factor):
        self.slice = slice
        self.smoothing_factor = smoothing_factor
        self.contours = []
        self.remaining_edge_points = EdgeDetector(self.slice).get_edge_points()

    def working_next_contour(self, slice):
        edge_points = EdgeDetector(self.slice).get_edge_points()
        return (
            ContourBuilder(edge_points).build(self.smoothing_factor)
        )


    def get_contours(self, loops):
        
        contours = [
            self.get_next_contour() for _ in range(loops)
        ]
        
        return( contours )

    def get_next_contour(self):
        

        contour = ContourBuilder(self.remaining_edge_points.copy()).build(self.smoothing_factor)
        contour_poly = Polygon(contour.vertices)

        return ( self.remaining_edge_points )

        
        
        
                
        for (x, y) in self.remaining_edge_points:
            point = Point(x, y)
            if point.within(contour_poly.buffer(100000)) or ((x, y) in contour.vertices):
                self.remaining_edge_points.remove((x, y))

        return ( self.remaining_edge_points )

