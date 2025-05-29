#!/usr/bin/env python3
''' Test Cases for PDF and DOCX parser functions in
module: app/models/parser.py

This module uses pytest to verify that the PDF and Word document parsing
functions behave as expected. We test for proper extraction of text, handling
of invalid input, and correct routing in the unified parser function.
Duck typing is applied in the sense that our functions expect objects with
the required methods (e.g., file names with a .lower() method) without
enforcing strict types.
'''

import os
import pytest
from app.models.parser import parse_pdf, parse_word, parse_document

# ------ Helper Function(s) ------ #


def get_test_file(file_name: str) -> bytes:
    '''
    Helper function to load sample test files from the tests directories.

    Args:
        file_name(str): Name of the file to load.

    Returns:
        bytes: The file content.
    '''
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    with open(file_path, 'rb') as f:
        return f.read()

# ------ Tests for PDF Parsing------ #


def test_parse_pdf_valid():
    '''
    Test that a valid PDF file is parsed correctly and returns
    expected text content.
    '''
    file_bytes = get_test_file('CHRIX ELEDU.pdf')
    text = parse_pdf(file_bytes)
    # Check that the extracted text contains the expected substring
    assert 'web infrastructure' in text.lower(), (
        'The PDF parser failed to extract text from file'
    )


def test_parse_pdf_empty():
    '''
    Test that attempting to parse an empty PDF raises a ValueError
    indicating that no text was extracted.
    '''
    file_bytes = b''
    with pytest.raises(ValueError, match='Empty PDF file: no text extracted.'):
        parse_pdf(file_bytes)


def test_parse_pdf_invalid_header():
    '''
    Test that a PDF without a valid PDF header raises a ValueError
    indicating an invalid PDF file.
    '''
    # Simulate a file that doesn't begin with the PDF header (%PDF-)
    file_bytes = b'Not a PDF file'
    with pytest.raises(
        ValueError,
        match='Invalid PDF file: Missing PDF header.'
    ):
        parse_pdf(file_bytes)

        

# ------  Tests for Word Parsing------ #


def test_parse_word_valid(monkeypatch):
    '''
    Test that a valid Word document is parsed correctly.
    This test uses monkeypatch to simulate a successful
    Tika response to avoid hanging.
    '''
    monkeypatch.setattr(
        'app.models.parser.tika_parser.from_buffer',
        lambda x: {'content': 'Test resume sample text'}
    )
    file_bytes = get_test_file('sample_resume.doc')
    text = parse_word(file_bytes, 'sample_resume.doc')
    assert 'test resume' in text.lower(), (
        'The word parser did not extract the expected text'
    )


def test_parse_word_empty():
    '''
    Test that attempting to parse an empty Word document
    raises a ValueError.
    '''
    file_bytes = b''
    with pytest.raises(
        ValueError,
        match='Empty Word document: no content provided.'
    ):
        parse_word(file_bytes, 'sample_resume.doc')


def test_parse_word_corrupt_empty_content(monkeypatch):
    '''
    Test that a Word documeent that Tika processes and
    returns empty content raises a ValueError.
    This simulates a case where Tika returns {'content': ''}
    without throwing an exception.
    '''
    monkeypatch.setattr(
        'app.models.parser.tika_parser.from_buffer',
        lambda x: {'content': ''}
    )
    file_bytes = b'This is not a valid Word file that yields content'
    with pytest.raises(
        ValueError,
        match='Empty Word document: no text extracted.'
    ):
        parse_word(file_bytes, 'sample_resume.doc')


def test_parse_word_exception(monkeypatch):
    '''
    Test that when Apache Tika raises an exception, parse_word
    raises a ValueError with the appropriate message.
    '''
    # Define a dummy function to simulate an exception in Tika.
    def fake_from_buffer(_):
        raise Exception('Simulated Tika failure')
    # Monkey-patch the tika_parser.from_buffer function in the parser module.
    monkeypatch.setattr(
        'app.models.parser.tika_parser.from_buffer',
        fake_from_buffer
    )

    with pytest.raises(
        ValueError,
        match='Error processing the document through Tika.'
    ):
        parse_word(b'dummy data', 'invalid.doc')


def test_parse_word_unicode(monkeypatch):
    '''
    Test that the Word parser correctly returns non-ASCII characters.
    '''
    # Sample content with non-ASCII characters
    unicode_content = 'Résumé – Éducation: Université de Genève' * 100

    monkeypatch.setattr(
        'app.models.parser.tika_parser.from_buffer',
        lambda x: {'content': unicode_content}
    )
    file_bytes = get_test_file('sample_resume.doc')
    text = parse_word(file_bytes, 'sample_resume.doc')
    assert 'université de genève' in text.lower(), (
        'Unicode text not properly extracted'
    )

# ------ Tests for Unified Document Parsing ------ #


def test_parse_document_pdf():
    '''
    Test that the unified parser routes PDF files correctly to
    the PDF parser.
    '''
    file_bytes = get_test_file('CHRIX ELEDU.pdf')
    text = parse_document(file_bytes, 'CHRIX ELEDU.pdf')
    assert 'web infrastructure' in text.lower(), (
        'Unified parser failed to correctly parse a Word document.'
    )


def test_parse_document_word(monkeypatch):
    '''
    Test that the unified parser routes Word documents correctly to
    the Word parser.
    '''
    monkeypatch.setattr(
        'app.models.parser.tika_parser.from_buffer',
        lambda x: {'content': 'Test resume sample text'}
    )
    file_bytes = get_test_file('sample_resume.doc')
    text = parse_document(file_bytes, 'sample_resume.doc')
    assert 'test resume' in text.lower(), (
        'Unified parser failed to correctly parse a Word document.'
    )


def test_parse_document_unsupported_file():
    '''
    Test that the unified parser raises a ValueError for unsupported
    file types.
    '''
    file_bytes = b'Random bytes data'
    with pytest.raises(ValueError, match='Unsupported file type.'):
        parse_document(file_bytes, 'unsupported_file.txt')

def test_parse_document_uppercase_extension(monkeypatch):
    '''
    Test that parse_document handles file names with uppercase extensions.
    '''
    monkeypatch.setattr(
        'app.models.parser.tika_parser.from_buffer',
        lambda x: {'content': 'Sample Text from Word'}
    )
    # Use an uppercase .DOC extension
    file_bytes = get_test_file('sample_resume.doc')
    text = parse_document(file_bytes, 'SAMPLE_RESUME.DOC')
    assert 'sample text' in text.lower(), (
        'Unified parser did not correctly handle uppercase file extension.'
    )
