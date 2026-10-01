import pydicom
import tempfile
import datetime
import json
from pydicom.sequence import Sequence
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import generate_uid

def generate_dicom_from_json(input_json):

    input_json_str = json.dumps(input_json)

    suffix = '.dcm'
    filename = tempfile.NamedTemporaryFile(suffix=suffix).name

    BasicTextSRIOD = '1.2.840.10008.5.1.4.1.1.88.11'

    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = BasicTextSRIOD
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.ImplementationClassUID = '1.3.46.670589.50.1.8.0'
    file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'

    ds = FileDataset(filename, {}, file_meta=file_meta, preamble=b"\0" * 128)

    ds.is_little_endian = True
    ds.is_implicit_VR = False

    dt = datetime.datetime.now()
    ds.ContentDate = dt.strftime('%Y%m%d')
    ds.ContentTime = dt.strftime('%H%M%S.%f')

    ds.SOPClassUID = BasicTextSRIOD

    ds.Modality = 'SR'
    ds.SpecificCharacterSet = 'ISO_IR 100' 
    
    sub_block = Dataset()
    sub_block.CodeValue = 'CODE_01'
    sub_block.CodingSchemeDesignator = 'NA'
    sub_block.CodeMeaning = 'CAD Summary'

    block = Dataset()
    block.RelationshipType = "CONTAINS"
    block.ValueType = "TEXT"
    block.ConceptNameCodeSequence = Sequence([sub_block])
    block.TextValue = input_json_str

    ds.ContentSequence = Sequence([block])

    # TODO:
    ds.SeriesNumber = series_number
    ds.SOPInstanceUID = generate_uid()
    ds.SeriesInstanceUID = generate_uid()
    ds.SeriesDescription = series_description
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
