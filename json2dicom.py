import pydicom
import tempfile
import datetime
import json
from pydicom.sequence import Sequence
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import generate_uid
from pydicom.uid import ExplicitVRLittleEndian, BasicTextSRStorage, PYDICOM_IMPLEMENTATION_UID

def generate_dicom_from_json(input_json, series_number, ref_dcm_obj=None, series_description="JSON"):

    sop_instance_uid = generate_uid()
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

if __name__ == "__main__":

    ds = generate_dicom_from_json({'test':'ok'})
    ds.save_as("ok.dcm")

"""

docker run -it -w /opt/workdir -v $PWD:/opt/workdir pangyuteng/dcm:latest bash


"""

"""
(0040, a040) Value Type                          CS: 'CONTAINER'
(0040, a043)  Concept Name Code Sequence  1 item(s) ----
   (0008, 0000) Group Length                        UL: 56
   (0008, 0100) Code Value                          SH: 'SYN-RPRT'
   (0008, 0102) Coding Scheme Designator            SH: '99SYN'
   (0008, 0104) Code Meaning                        LO: 'Diagnostic Report'
   ---------
(0040, a050) Continuity Of Content               CS: 'SEPARATE'
(0040, a372)  Performed Procedure Code Sequence  1 item(s) ----

   ---------
(0040, a491) Completion Flag                     CS: 'COMPLETE'
(0040, a493) Verification Flag                   CS: 'UNVERIFIED'
(0040, a730)  Content Sequence  1 item(s) ----
   (0040, 0000) Group Length                        UL: 2136
   (0040, a010) Relationship Type                   CS: 'CONTAINS'
   (0040, a040) Value Type                          CS: 'TEXT'
   (0040, a043)  Concept Name Code Sequence  1 item(s) ----
      (0008, 0000) Group Length                        UL: 48
      (0008, 0100) Code Value                          SH: 'CODE_01'
      (0008, 0102) Coding Scheme Designator            SH: '99SYN'
      (0008, 0104) Code Meaning                        LO: 'Diagnosis'
      ---------
   (0040, a160) Text Value                          UT: Array of 2023 elements

# ds[(0x0040, 0xa730)][0][(0x0040, 0xa160)].value

"""
