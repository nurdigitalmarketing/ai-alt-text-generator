# streamlit_app.py

import streamlit as st
import requests
import base64
from PIL import Image
import io
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Title of the Streamlit app
st.title('AltText.ai Integration with Streamlit')

# API key input
API_KEY = st.text_input("Enter your AltText.ai API key:", type="password")

# Language selector
languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it"
}
selected_language = st.selectbox("Select language for alt text:", list(languages.keys()))

# File uploader for multiple images
uploaded_files = st.file_uploader("Choose images...", type=["jpg", "png", "jpeg", "gif", "webp"], accept_multiple_files=True)

def generate_alt_text(image_file, api_key, language):
    """Call the AltText.ai API to generate alt text for the given image."""
    url = "https://alttext.ai/api/v1/images"
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    # Convert image to base64
    img = Image.open(image_file)
    buffered = io.BytesIO()
    img.save(buffered, format=img.format)
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    data = {
        "image": {
            "raw": img_str
        },
        "lang": language
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    logging.info(f"Request to AltText.ai API: {response.request.body}")
    logging.info(f"Response from AltText.ai API: {response.status_code}, {response.text}")
    
    return response

if API_KEY and uploaded_files:
    st.write(f"Generating alt text in {selected_language}...")
    for uploaded_file in uploaded_files:
        # Generate alt text for each uploaded image
        alt_text_response = generate_alt_text(uploaded_file, API_KEY, languages[selected_language])
        
        if alt_text_response.status_code == 200:
            response_json = alt_text_response.json()
            alt_text = response_json.get('alt_text', 'No alt text generated')
            metadata = response_json.get('metadata', {})
            st.write(f"Generated Alt Text for {uploaded_file.name}: {alt_text}")
            st.write(f"Metadata: {metadata}")
        else:
            error_details = alt_text_response.json()
            error_code = error_details.get('error_code', 'Unknown error code')
            errors = error_details.get('errors', 'No error details available')
            st.write(f"Error in generating alt text for {uploaded_file.name}: {error_code}")
            st.write(f"Error details: {errors}")

# To run this Streamlit app, save this code in a file named `app.py` and run `streamlit run app.py` in your terminal.
