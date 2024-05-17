import pytest
import requests
from unittest.mock import patch, Mock

from app import generate_alt_text

# Mock API key for testing
API_KEY = "TEST_API_KEY"

def test_generate_alt_text():
    image_data = b'test_image_data'
    with patch('builtins.open', new_callable=Mock) as mock_open:
        mock_open.return_value.read.return_value = image_data
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'alt_text': 'A test alt text'}
            mock_post.return_value = mock_response
            
            # Open a dummy image file
            with open('dummy.jpg', 'rb') as img_file:
                response = generate_alt_text(img_file)
            
            assert response.status_code == 200
            assert response.json().get('alt_text') == 'A test alt text'

def test_generate_alt_text_error():
    image_data = b'test_image_data'
    with patch('builtins.open', new_callable=Mock) as mock_open:
        mock_open.return_value.read.return_value = image_data
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 400
            mock_response.json.return_value = {'error_code': 'invalid_request', 'errors': 'Invalid image data'}
            mock_post.return_value = mock_response
            
            # Open a dummy image file
            with open('dummy.jpg', 'rb') as img_file:
                response = generate_alt_text(img_file)
            
            assert response.status_code == 400
            assert response.json().get('error_code') == 'invalid_request'
            assert response.json().get('errors') == 'Invalid image data'
