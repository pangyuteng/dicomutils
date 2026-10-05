
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
