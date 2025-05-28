#!/usr/bin/env python3
''' PDF and DOCX parser functions to extract
text from bytes in PDF and DOC files respectively
'''

import io
import docx
from docx.opc.exceptions import PackageNotFoundError
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFSyntaxError


def parse_pdf(file_bytes: bytes) -> str:
    ''' Parser function for PDF files'''
    # First check the file header to see if it starts with the PDF signature
    if not file_bytes.startswith(b'%PDF-'):
        raise ValueError('Invalid PDF file: Missing PDF header.')
    output_string = io.StringIO()

    # Use BytesIO to wrap the byte stream for pdfminer
    try:
        with io.BytesIO(file_bytes) as file_stream:
            # Adjust LAParams if needed to tune layout analysis
            laparams = LAParams()
            extract_text_to_fp(file_stream, output_string, laparams=laparams)
    except PDFSyntaxError as e:
        # This exception indicates a parsing error,
        # so the PDF is likely corrupt
        raise ValueError('Corrupt PDF file: cannot extract text') from e

    text = output_string.getvalue().strip()
    if not text:
        raise ValueError('Empty PDF file: no text extracted')
    return text


def parse_docx(file_bytes: bytes) -> str:
    ''' Parser function for DOC files'''
    if not file_bytes:
        raise ValueError('Empty DOCX file: no content provided')
    try:
        # Attempt to parse using python-docx
        doc = docx.Document(io.BytesIO(file_bytes))
    except PackageNotFoundError as e:
        raise ValueError('Invalid or corrupt DOCX file') from e

    text = " ".join(para.text for para in doc.paragraphs).strip()
    return text
