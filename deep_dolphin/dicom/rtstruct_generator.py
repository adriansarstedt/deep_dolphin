import pydicom
from pydicom.dataset import Dataset
from pydicom.sequence import Sequence
from pydicom.uid import generate_uid
from pydicom import dcmread
from datetime import date
import time

from deep_dolphin.dicom.dicom_study_parser import DicomStudyParser

def save_rt_struct(output_path, dicom_dir_path, series_protocol, contours):
    rt_struct = generate_rt_struct(dicom_dir_path, series_protocol, contours)
    rt_struct.save_as(output_path, write_like_original=False)

def generate_rt_struct(dicom_dir_path, series_protocol, contours):
    referenced_study = DicomStudyParser(dicom_dir_path)
    referenced_series =  referenced_study.get_series(series_protocol)

    ds = Dataset()
    ds.file_meta = generate_rtstruct_meta()
    ds.is_implicit_VR = False
    ds.is_little_endian = True

    populate_generic_tags(ds)
    populate_description_tags(ds)
    populate_datetime_tags(ds)
    populate_roi_details(ds)
    populate_inherited_study_tags(ds, referenced_study)
    populate_inherited_series_tags(ds, referenced_series)
    populate_frame_of_reference(ds, referenced_study, referenced_series)
    populate_contour_sequence(ds, referenced_series, contours)

    return (ds)
    

def populate_generic_tags(ds):
    ds.SpecificCharacterSet = 'ISO_IR 192'
    ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.481.3'
    ds.Modality = 'RTSTRUCT'
    ds.Manufacturer = 'MIM Software Inc.'
    ds.ManufacturerModelName = 'MIM'
    ds.SoftwareVersions = '6.4.5'
    ds.SOPInstanceUID = generate_uid()
    ds.SeriesInstanceUID = generate_uid()

def populate_description_tags(ds):
    name = 'DeepDolphin Segmentation'
    label = 'RTstruct'
    description = 'This is a segmentation made by deepdolphin' 
    ds.StructureSetName = name
    ds.StructureSetLabel = label
    ds.SeriesDescription = description
    ds.SeriesNumber = "1"

def populate_datetime_tags(ds):
    formatted_date = str(date.today()).replace('-', '')
    formatted_time = time.strftime("%H%M%S", time.localtime())
    ds.InstanceCreationDate = formatted_date
    ds.InstanceCreationTime = formatted_time
    ds.SeriesDate = formatted_date
    ds.SeriesTime = formatted_time
    ds.StructureSetDate = formatted_date
    ds.StructureSetTime = formatted_time

def populate_inherited_study_tags(ds, referenced_study):
    ds.StudyInstanceUID = referenced_study.get('StudyInstanceUID')
    ds.StudyID = referenced_study.get('StudyID')
    ds.StudyDate = referenced_study.get('StudyDate')
    ds.StudyTime = referenced_study.get('StudyTime')
    ds.StudyDescription = referenced_study.get('StudyDescription')
    ds.AccessionNumber = referenced_study.get('AccessionNumber')

def populate_inherited_series_tags(ds, referenced_series):
    ds.InstitutionName = referenced_series.get('InstitutionName')
    ds.StationName = referenced_series.get('StationName')
    ds.ReferringPhysicianName = referenced_series.get('ReferringPhysicianName')
    ds.OperatorsName = referenced_series.get('OperatorsName')
    ds.PatientName = referenced_series.get('PatientName')
    ds.PatientID = referenced_series.get('PatientID')
    ds.PatientBirthDate = referenced_series.get('PatientBirthDate')

def populate_frame_of_reference(ds, referenced_study, referenced_series):
    frame_of_reference_sequence = Sequence()
    frame_of_reference_1 = Dataset()
    study_sequence = Sequence()
    study_1 = Dataset()
    series_sequence = Sequence()
    series_1 = Dataset()
    image_sequence = Sequence()

    frame_of_reference_1.RTReferencedStudySequence = study_sequence
    study_1.RTReferencedSeriesSequence = series_sequence
    series_1.ContourImageSequence = image_sequence

    frame_of_reference_1.FrameOfReferenceUID = referenced_series.get('FrameOfReferenceUID')
    study_1.ReferencedSOPClassUID = referenced_study.get('SOPClassUID')
    study_1.ReferencedSOPInstanceUID = referenced_study.get('StudyInstanceUID')
    series_1.SeriesInstanceUID = referenced_series.get('SeriesInstanceUID')

    for uid in referenced_series.referenced_uids():
        image = Dataset()
        image.ReferencedSOPClassUID = '1.2.840.10008.5.1.4.1.1.4'
        image.ReferencedSOPInstanceUID = uid
        image_sequence.append(image)

    series_sequence.append(series_1)
    study_sequence.append(study_1)
    frame_of_reference_sequence.append(frame_of_reference_1)
    ds.ReferencedFrameOfReferenceSequence = frame_of_reference_sequence

def populate_contour_sequence(ds, referenced_series, contours):
    structure_set_roi_sequence = Sequence()
    
    structure_set_roi1 = Dataset()
    structure_set_roi1.SpecificCharacterSet = 'ISO_IR 192'
    structure_set_roi1.ROINumber = "1"
    structure_set_roi1.ReferencedFrameOfReferenceUID = referenced_series.get('FrameOfReferenceUID')
    structure_set_roi1.ROIName = 'FLAIR'
    structure_set_roi1.ROIDescription = ''
    structure_set_roi1.ROIGenerationAlgorithm = 'DeepDolphin'
    structure_set_roi_sequence.append(structure_set_roi1)

    roi_contour_sequence = Sequence()
    ds.ROIContourSequence = roi_contour_sequence

    roi_contour1 = Dataset()
    roi_contour1.ROIDisplayColor = [255, 0, 255]

    contour_sequence = Sequence()
    roi_contour1.ContourSequence = contour_sequence

    for dicom_slice in contours:

        dicom_uid = referenced_series.referenced_uids()[dicom_slice]
        contour_image_sequence = Sequence()

        referenced_image = Dataset()
        referenced_image.ReferencedSOPClassUID = '1.2.840.10008.5.1.4.1.1.4'
        referenced_image.ReferencedSOPInstanceUID = dicom_uid
        contour_image_sequence.append(referenced_image)

        for contour_set in contours[dicom_slice]:
            contour = Dataset()
            contour.ContourImageSequence = contour_image_sequence
            contour.ContourGeometricType = 'CLOSED_PLANAR'
            contour.NumberOfContourPoints = len(contour_set)/3
            contour.ContourData = contour_set
            contour_sequence.append(contour)

    roi_contour1.ReferencedROINumber = "1"
    roi_contour_sequence.append(roi_contour1)

    ds.StructureSetROISequence = structure_set_roi_sequence

def populate_roi_details(ds):
    rtroi_observations_sequence = Sequence()
    ds.RTROIObservationsSequence = rtroi_observations_sequence

    rtroi_observations1 = Dataset()
    rtroi_observations1.ObservationNumber = "1"
    rtroi_observations1.ReferencedROINumber = "1"
    rtroi_observations1.ROIObservationDescription = 'Type:Soft, Range:*/*, Fill:0, Opacity:0.0, Thickness:1, LineThickness:2, finding:Finding 1'
    rtroi_observations1.RTROIInterpretedType = ''
    rtroi_observations1.ROIInterpreter = ''
    rtroi_observations_sequence.append(rtroi_observations1)

    ds.ApprovalStatus = 'UNAPPROVED'

def generate_rtstruct_meta():
    file_meta = Dataset()
    file_meta.FileMetaInformationGroupLength = 216
    file_meta.FileMetaInformationVersion = b'\x00\x01'
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.481.3'
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.4.90'
    file_meta.ImplementationClassUID = '1.2.276.0.7238010.5.0.3.5.4'
    file_meta.ImplementationVersionName = 'OSIRIX'
    file_meta.SourceApplicationEntityTitle = 'MIM'
    return (file_meta)