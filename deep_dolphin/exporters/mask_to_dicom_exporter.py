# will be used to convert model output mask into a
# format able to be transported and viewed in dicom software

from deep_dolphin.contouring.contour_builder import ContourBuilder

class MaskToDicomExporter(object):

    def __init__(self, nii_mask_path, dicom_dir_path, protocol_name, nii_dir_path=None):
        self.mask_path = mask_path
        self.dicom_dir_path = dicom_dir_path
        self.protocol_name = protocol_name

    def get_contour_for_mask_slice(self, mask_slice, smoothing_factor):
        edge_points = self.get_edge_points_for_mask_slice(mask_slice)
        contour = ContourBuilder(edge_points).build(smoothing_factor)
        return( contour )

    def get_edge_points_for_mask_slice(self, mask_slice):
        edge_points = []
        for x in range(1, len(mask_slice)-1):
            for y in range(1, len(mask_slice[0])-1):
                if self.is_non_zero(x, y, mask_slice) and self.is_edge_point(x, y, mask_slice):
                    edge_points.append((x, y))
        return( edge_points )

    def is_edge_point(self, x, y, mask):
        return (
            (mask[x+1][y] == 0) or
            (mask[x-1][y] == 0) or
            (mask[x][y+1] == 0) or
            (mask[x][y-1] == 0)
        )

    def is_non_zero(self, x, y, mask):
        return (
            mask[x][y] != 0
        )

