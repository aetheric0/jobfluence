#!/usr/bin/env python3
'''
Test Cases for the file upload endpoint that enforces a file size cap.
We verify that:
- A file within the allowed size is successfully processed.
- A file exceeding the allowed size is rejected.
'''

import io
import pytest
from fastapi.testclient import TestClient
from app.main import app
from config import settings

client = TestClient(app)


def test_upload_resume_small_file(monkeypatch):
    '''
    Test that an uploaded resume that is within the allowed file size
    is processed. We use monkeypatch to simulate Tika's response to
    avoid external dependencies.
    '''
    # Patch Tika's response to simulate a successful extraction
    monkeypatch.setattr(
        'app.models.parser.extract_text_to_fp',
        lambda file_stream, output, laparams: output.write(
            'Test resume sample text'
        )
    )

    # Create a fake, small PDF file (with valid PDF header)
    small_file = io.BytesIO(b'%PDF- valid content')
    # Simulate a file upload
    response = client.post(
        '/parser/extract',
        files={'file': ('resume.pdf', small_file, 'application/pdf')}
    )
    # Expecting HTTP 200 OK if processing is successful
    assert response.status_code == 200, response.text
    assert 'extracted_text' in response.json()
    assert 'test resume' in response.json()['extracted_text'].lower()

def test_upload_resume_file_too_large():
    '''
    Test that an uploaded resume exceeding the allowed file size is
    rejected
    '''
    # Generate a file larger than MAX_FILE_SIZE
    large_file = io.BytesIO(b'A' * (settings.MAX_FILE_SIZE + 1))

    response = client.post(
        '/parser/extract',
        files={'file': ('large_resume.pdf', large_file, 'application/pdf')}
    )
    # Expect a 413 Payload Too Large error
    assert response.status_code == 413, response.text
    # Optionally, check that the error detail contains teh expected message
    assert 'File too large' in response.json().get('detail', '')
