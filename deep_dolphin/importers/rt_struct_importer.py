import pydicom

from deep_dolphin.dicom.dicom_series_parser_2 import DicomSeriesParser2


class RTStructImporter(object):
    def convert(self, rtstruct_path, dicom_path):
        rtstruct = pydicom.dcmread(rtstruct_path)
        referenced_series_uid = (
            rtstruct.ReferencedFrameOfReferenceSequence[0]
            .RTReferencedStudySequence[0]
            .RTReferencedSeriesSequence[0]
            .SeriesInstanceUID
        )

        series = DicomSeriesParser2(dicom_path, series_uid=referenced_series_uid)
        print(referenced_series_uid)
        # dicom_series = DicomSeriesParser(dicom_path)

