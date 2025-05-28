#!/usr/bin/env python3
''' Test Cases for PDF and DOCX parser functions in
module: app/models/parser.py
'''

import os
import pytest
from app.models.parser import parse_pdf, parse_docx


# ------ Helper Function(s) ------ #

def get_test_file(file_name: str) -> bytes:
    '''Helper function to load sample
    test files from the current tests directories'''
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    with open(file_path, 'rb') as f:
        return f.read()


# ------ PDF Parser Test Cases ------ #

def test_parse_pdf_valid():
    '''Test that a valid PDF file is parsed correctly.'''
    file_bytes = get_test_file('Chrix Eledu.pdf')
    text = parse_pdf(file_bytes)
    # Check that the extracted text contains the expected substring
    assert 'web infrastructure' in text, 'The PDF parser failed '
    'to extract text from file'


def test_parse_pdf_empty():
    '''Tests that an empty byte stream returns an empty string.'''
    file_bytes = b''
    with pytest.raises(ValueError, match='no text extracted'):
        parse_pdf(file_bytes)


def test_parse_pdf_invalid_header():
    '''Test that a PDF without a valid header is rejected as invalid.'''
    # Simulate a file that doesn't begin with the PDF header (%PDF-)
    file_bytes = b'Not a PDF file'
    with pytest.raises(ValueError, match='Missing PDF header'):
        parse_pdf(file_bytes)


# ------ DOCX Parser Test Cases ------ #
def test_parse_docx_valid():
    '''Test that a valid DOCX file is parsed correctly.'''
    file_bytes = get_test_file('sample_resume.doc')
    text = parse_docx(file_bytes)
    assert 'Test Resume' in text, 'The DOCX parser did not '
    'extract the expected text'


def test_parse_docx_empty():
    '''Test that na empty DOCX byte stream raises an error.'''
    file_bytes = b''
    with pytest.raises(ValueError, match='Empty DOCX file'):
        parse_docx(file_bytes)


def test_parse_docx_corrupt():
    '''Test that a corrupt DOCX file raises an error.'''
    # Simulate a corrupt DOCX file by providing invalid bytes
    file_bytes = b'This is not a valid docx file.'
    with pytest.raises(ValueError, match='Invalid or corrupt DOCX file'):
        parse_docx(file_bytes)
