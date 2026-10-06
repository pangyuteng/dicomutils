
```

providing below options for saving json/csv (text) to dicom:

 + (preferred?) create a structured report, see json2dicom.py

 + save as text or binary to private tag, see https://grok.com/share/bGVnYWN5_3247a87d-5aae-4e44-8bc8-5cf544f9b16c

 + can you embed the csv or json file just like pdf?

```

https://highdicom.readthedocs.io/en/latest/quickstart.html#creating-structured-report-sr-documents

https://pydicom.github.io/pydicom/stable/tutorials/sr_basics.html

https://grok.com/share/bGVnYWN5_3247a87d-5aae-4e44-8bc8-5cf544f9b16c

https://github.com/rohithkumar31/pdf2dicom/blob/master/pdf2dicom.py

https://www.dicomstandard.org/docs/librariesprovider2/dicomdocuments/wp-cotent/uploads/2018/10/day2_s1-solomon-deep-dive-into-sr.pdf?sfvrsn=45f072fb_4

https://dicom.nema.org/dicom/2013/output/chtml/part04/sect_i.4.html

https://dicom.innolitics.com/ciods/enhanced-sr/sr-document-content/0040a730

https://github.com/OHIF/Viewers/issues/64

"Basic Text SR IOD" 1.2.840.10008.5.1.4.1.1.88.11



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
