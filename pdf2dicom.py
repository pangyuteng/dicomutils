# copied from https://github.com/rohithkumar31/pdf2dicom/blob/master/pdf2dicom.py

import pydicom
import tempfile
import datetime
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import generate_uid
from pydicom.uid import ExplicitVRLittleEndian, EncapsulatedPDFStorage, PYDICOM_IMPLEMENTATION_UID

def generate_dicom_from_pdf(pdf_file, series_number, 
    sop_instance_uid = None, series_instance_uid = None,
    ref_dcm_obj = None, series_description = "PDF",
    is_validate_file_meta = True):

    if sop_instance_uid is None:
        sop_instance_uid = generate_uid()

    if series_instance_uid is None:
        series_instance_uid = generate_uid()

    suffix = '.dcm'
    filename = tempfile.NamedTemporaryFile(suffix=suffix).name

    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = EncapsulatedPDFStorage
    file_meta.MediaStorageSOPInstanceUID = sop_instance_uid
    file_meta.ImplementationClassUID = PYDICOM_IMPLEMENTATION_UID
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    if is_validate_file_meta is True:
        pydicom.dataset.validate_file_meta(file_meta,enforce_standard=False)

    ds = FileDataset(filename, {}, file_meta=file_meta, preamble=b"\0" * 128)

    ds.is_little_endian = True
    ds.is_implicit_VR = False

    dt = datetime.datetime.now()
    ds.ContentDate = dt.strftime('%Y%m%d')
    ds.ContentTime = dt.strftime('%H%M%S.%f')

    ds.SOPClassUID = EncapsulatedPDFIOD
    ds.MIMETypeOfEncapsulatedDocument = 'application/pdf'
    ds.Modality = 'DOC' #document
    ds.ConversionType = 'WSD' #workstation
    ds.SpecificCharacterSet = 'ISO_IR 100' 
    # more codes for charecter encoding here https://dicom.innolitics.com/ciods/cr-image/sop-common/00080005 

    with open(pdf_file, 'rb') as f:
        f_read = f.read()
        ValueLength = len(f_read)
        ## All Dicom Element must have an even ValueLength
        if ValueLength % 2 != 0:
            f_read += b'\0'
        ds.EncapsulatedDocument = f_read

    ds.SeriesNumber = series_number
    ds.SOPInstanceUID = sop_instance_uid
    ds.SeriesInstanceUID = series_instance_uid
    ds.SeriesDescription = series_description
    
    if ref_dcm_obj is not None:
        ds.PatientID = ref_dcm_obj.PatientID
        ds.PatientName = ref_dcm_obj.PatientName
        ds.StudyDate = ref_dcm_obj.StudyDate
        ds.StudyInstanceUID = ref_dcm_obj.StudyInstanceUID
        ds.ReferencedSeriesSequence = [ref_dcm_obj]

    return ds