import pydicom
import tempfile
import datetime
import json
from pydicom.sequence import Sequence
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import generate_uid
from pydicom.uid import ExplicitVRLittleEndian, BasicTextSRStorage, PYDICOM_IMPLEMENTATION_UID

def generate_dicom_from_json(input_json, series_number, 
    sop_instance_uid = None, series_instance_uid = None,
    ref_dcm_obj = None, series_description = "JSON",
    is_validate_file_meta = True):

    if sop_instance_uid is None:
        sop_instance_uid = generate_uid()

    if series_instance_uid is None:
        series_instance_uid = generate_uid()

    suffix = '.dcm'
    filename = tempfile.NamedTemporaryFile(suffix=suffix).name

    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = BasicTextSRStorage
    file_meta.MediaStorageSOPInstanceUID = sop_instance_uid
    file_meta.ImplementationClassUID = PYDICOM_IMPLEMENTATION_UID
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    ds = FileDataset(filename, {}, file_meta=file_meta, preamble=b"\0" * 128)

    ds.is_little_endian = True
    ds.is_implicit_VR = False

    dt = datetime.datetime.now()
    ds.ContentDate = dt.strftime('%Y%m%d')
    ds.ContentTime = dt.strftime('%H%M%S.%f')

    ds.SOPClassUID = BasicTextSRIOD
    ds.Modality = 'SR'
    ds.SpecificCharacterSet = 'ISO_IR 100' 
    
    # NOTE: going against dicom sr standards, just dumping json to text.

    input_json_str = json.dumps(input_json)

    sub_item = Dataset()
    sub_item.CodeValue = 'CODE_01'
    sub_item.CodingSchemeDesignator = 'NA'
    sub_item.CodeMeaning = 'CAD Summary'

    item = Dataset()
    item.RelationshipType = "CONTAINS"
    item.ValueType = "TEXT"
    item.ConceptNameCodeSequence = Sequence([sub_item])
    item.TextValue = input_json_str

    ds.ContentSequence = Sequence([item])

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
