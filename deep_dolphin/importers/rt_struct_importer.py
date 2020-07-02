import pydicom
import numpy as np
import matplotlib.pyplot as plt

from deep_dolphin.dicom.dicom_series_parser_2 import DicomSeriesParser2
from deep_dolphin.dicom.dicom_coordinate_mapper import DicomCoordinateMapper
from deep_dolphin.contouring.set_to_contour_converter import SetToContourConverter


class RTStructImporter(object):
    def convert(self, rtstruct_path, dicom_path):
        rtstruct = pydicom.dcmread(rtstruct_path)
        referenced_series_uid = (
            rtstruct.ReferencedFrameOfReferenceSequence[0]
            .RTReferencedStudySequence[0]
            .RTReferencedSeriesSequence[0]
            .SeriesInstanceUID
        )

        # probably needs to be a check to remove duplicates in here
        series = DicomSeriesParser2(dicom_path, series_uid=referenced_series_uid)

        number_of_slices = max(
            map(lambda dicom: dicom.InstanceNumber, series.get_dicom_files())
        )
        number_of_rows = series.get_tag("Rows")
        number_of_columns = series.get_tag("Columns")
        pixel_map = np.zeros((number_of_columns, number_of_rows, number_of_slices))

        print("parsing contours")

        contours = rtstruct.ROIContourSequence[0].ContourSequence
        coordinate_mapper = DicomCoordinateMapper(
            dicom_path, "AXIAL FLAIR +C"
        )  # need to fix

        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import axes3d, Axes3D  # <-- Note the capitalization!

        X = []
        Y = []
        Z = []

        for contour in contours:
            print("contour starting")
            image_uid = contour.ContourImageSequence[0].ReferencedSOPInstanceUID
            image = series.get_file_by("SOPInstanceUID", image_uid)
            contour_data = contour.ContourData
            number_or_points = int(len(contour_data) / 3)
            points = []

            for i in range(number_or_points):
                x, y, z = (
                    contour_data[3 * i],
                    contour_data[3 * i + 1],
                    contour_data[3 * i + 2],
                )
                [i, j] = coordinate_mapper.patient_to_image_coordinates(x, y, z, image)
                points.append([i, j])

                X.append(i)
                Y.append(j)
                Z.append(image.InstanceNumber)

            from shapely.geometry import Polygon, Point, MultiPoint

            # https://stackoverflow.com/questions/44399749/get-all-lattice-points-lying-inside-a-shapely-polygon

            p = Polygon(points)
            xmin, ymin, xmax, ymax = p.bounds
            x = np.arange(np.floor(xmin), np.ceil(xmax) + 1)  # array([0., 1., 2.])
            y = np.arange(np.floor(ymin), np.ceil(ymax) + 1)  # array([0., 1., 2.])
            points = MultiPoint(
                np.transpose([np.tile(x, len(y)), np.repeat(y, len(x))])
            )
            result = points.intersection(p)

            layer = np.zeros(())

            for point in result:
                pixel_map[int(point.x), int(point.y), image.InstanceNumber] = 1

            # def get_surrounding_points(polygon):
            #     minx, miny, maxx, maxy = polygon.bounds
            #     minx, miny, maxx, maxy = int(minx), int(miny), int(maxx), int(maxy)
            #     return [
            #         Point([x, y])
            #         for x in range(minx, maxx + 1)
            #         for y in range(miny, maxy + 1)
            #     ]

            # polygon = Polygon(points)

            # surrounding_points = get_surrounding_points(polygon)
            # for point in surrounding_points:
            #     if polygon.contains(point):
            #         pixel_map[int(point.x), int(point.y), image.InstanceNumber] = 1

            # fig = plt.figure(figsize=(10, 12))
            # axes = fig.add_axes([0.15, 0.1, 0.7, 0.8])
            # axes.set_xlim([0, number_of_rows])
            # axes.set_ylim([0, number_of_columns])
            # axes.imshow(pixel_map[image.InstanceNumber, :, :])
            # plt.show()

        import nibabel as nib

        data = pixel_map

        fixture = nib.load("./fixtures/nii/original_flair.nii")
        print(fixture.affine)
        new_image = nib.Nifti1Image(data, affine=fixture.affine)
        nib.save(new_image, "./please.nii")
        fig = plt.figure()

        ax = Axes3D(fig)  # <-- Note the difference from your original code...
        cset = ax.scatter3D(X, Y, Z, cmap="hsv")

        ax.clabel(cset, fontsize=9, inline=1)
        plt.show()

        # contourer = SetToContourConverter(4)

        # points = contourer.convert(points)[0]

        # dicom_series = DicomSeriesParser(dicom_path)

