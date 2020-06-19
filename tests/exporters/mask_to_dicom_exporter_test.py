import unittest
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np


from deep_dolphin.contouring.contour_builder import ContourBuilder
from deep_dolphin.contouring.slice_contour_builder import SliceContourBuilder
from deep_dolphin.contouring.edge_detector import EdgeDetector

class MaskToDicomExporterTest(unittest.TestCase):

    def test_(self):
        example_mask_path = "./fixtures/output_mask.nii.gz"
        mask = nib.load(example_mask_path)

        (X, Y, Z) = mask.shape
        mask_data = mask.get_fdata()
        mask_slice = mask_data[100]

        fig = plt.figure(figsize=(10,12))
        axes = fig.add_axes([0.15,0.1,0.7,0.8])
        axes.set_xlim([0,Z])
        axes.set_ylim([0,Y])
        axes.imshow(mask_slice)

        from shapely.geometry import Point, Polygon

        edge_points = EdgeDetector(mask_slice).get_edge_points()
        (next_contour, unexplored_points) = ContourBuilder(edge_points).build(3)
        next_contour_poly = Polygon(next_contour.vertices)
        next_enlarged_contour_poly = next_contour_poly.buffer(2)

        remaining_edge_points = []
        for point in unexplored_points:
            point_ = Point(point)
            if not point_.within(next_enlarged_contour_poly):
                    remaining_edge_points.append(point)

        (next_next_contour, next_unexplored_points) = ContourBuilder(remaining_edge_points).build(4)
        next_next_contour_poly = Polygon(next_contour.vertices)
        next_next_enlarged_contour_poly = next_next_contour_poly.buffer(3)

        next_remaining_edge_points = []
        for point in next_unexplored_points:
            point_ = Point(point)
            if not point_.within(next_next_enlarged_contour_poly):
                    next_remaining_edge_points.append(point)

        xs, ys = np.array(next_contour.vertices)[:,1], np.array(next_contour.vertices)[:,0]
        axes.plot(xs,ys, 'go--', linewidth=2, markersize=5)
                
        xs, ys = np.array(remaining_edge_points)[:,1], np.array(remaining_edge_points)[:,0]
        axes.plot(xs,ys, 'bo--', linewidth=0, markersize=3)

        xs, ys = np.array(next_next_contour.vertices)[:,1], np.array(next_next_contour.vertices)[:,0]
        axes.plot(xs,ys, 'ro--', linewidth=1, markersize=3)

        plt.show()

        """
        for point in next_contour.vertices:

        a = SliceContourBuilder(mask_slice, 3).get_contours(2)
        
        
        count = 0
        for contour in a:
            
            
            
            xs, ys = np.array(contour)[:,1], np.array(contour)[:,0]
            if count==0:
                axes.plot(xs,ys, 'go--', linewidth=0, markersize=10)
            else:
                axes.plot(xs,ys, 'bo--', linewidth=0, markersize=4)
            count += 1
        """
    
        

        """
        for p in a:
            plt.scatter(p[0], p[1], 100)

        plt.show()

        for p in b:
            plt.scatter(p[0], p[1], 100)

        plt.show()
        """
        
        self.assertEqual(1, 2)


        """
        contour = SliceContourBuilder(mask_slice).get_contours(3)
        
        
        if contour.is_valid():
            xs, ys = np.array(contour.vertices)[:,1], np.array(contour.vertices)[:,0]
            axes.plot(xs,ys)
        """
        plt.show()



if __name__ == '__main__':
    unittest.main()
