import streamlit as st
import requests
import base64
from PIL import Image
import io
import logging
import pandas as pd

# Crea una riga con 3 colonne
col1, col2 = st.columns([1, 7])

# Colonna per l'immagine (a sinistra)
with col1:
    st.image("https://raw.githubusercontent.com/nurdigitalmarketing/previsione-del-traffico-futuro/9cdbf5d19d9132129474936c137bc8de1a67bd35/Nur-simbolo-1080x1080.png", width=80)

# Colonna per il titolo e il testo "by NUR® Digital Marketing" (al centro)
with col2:
    st.title('AI Alt Text Generator')
    st.markdown('###### by [NUR® Digital Marketing](https://www.nur.it)')

st.markdown("""

## Introduzione

L'applicazione consente di caricare più immagini, selezionare la lingua del testo alternativo e generare il codice HTML con il testo alternativo. I risultati possono essere esportati in un file Excel.
    """)

with st.expander("Istruzioni"):
    st.markdown("""
    1. **Inserisci la tua API Key:**
       - Nella casella di testo, inserisci la tua [API key di AltText.ai](https://alttext.ai/account/api_keys).

    2. **Seleziona la Lingua:**
       - Utilizza il selettore a tendina per scegliere la lingua in cui desideri generare il testo alternativo.

    3. **Carica le Immagini:**
       - Usa il pulsante di caricamento per selezionare e caricare le immagini dal tuo dispositivo.

    4. **Genera Alt Text:**
       - Una volta caricate le immagini, l'applicazione genererà automaticamente il testo alternativo per ciascuna immagine.

    5. **Esporta in Excel:**
       - Dopo la generazione del testo alternativo, puoi esportare i risultati in un file Excel cliccando sul pulsante di esportazione.
    """)

st.markdown('---')

# Set up logging
logging.basicConfig(level=logging.INFO)

# API key input
API_KEY = st.text_input("Inserisci la tua chiave API da [AltText.ai](https://alttext.ai/account/api_keys):", type="password")

# Language selector
languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it"
}
selected_language = st.selectbox("Selezionare la lingua per l'alt text:", list(languages.keys()))

# File uploader for multiple images
uploaded_files = st.file_uploader("Scegli immagini...", type=["jpg", "png", "jpeg", "gif", "webp"], accept_multiple_files=True)

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

# Prepare data for DataFrame
results = []

if API_KEY and uploaded_files:
    st.write(f"Generating alt text in {selected_language}...")
    for uploaded_file in uploaded_files:
        # Generate alt text for each uploaded image
        alt_text_response = generate_alt_text(uploaded_file, API_KEY, languages[selected_language])
        
        if alt_text_response.status_code == 200:
            response_json = alt_text_response.json()
            alt_text = response_json.get('alt_text', 'No alt text generated')
            html_code = f'<img src="{uploaded_file.name}" alt="{alt_text}">'
            results.append([uploaded_file.name, alt_text, html_code])
        else:
            error_details = alt_text_response.json()
            error_code = error_details.get('error_code', 'Unknown error code')
            errors = error_details.get('errors', 'No error details available')
            st.write(f"Error in generating alt text for {uploaded_file.name}: {error_code}")
            st.write(f"Error details: {errors}")

# Display results in a table
if results:
    df = pd.DataFrame(results, columns=["Image Name", "Alt Text", "HTML Code"])
    st.write(df)

    # Export to Excel
    if st.button("Export to Excel"):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='AltText')
            writer.save()
        st.download_button(label="Download Excel file", data=output.getvalue(), file_name="alt_text_results.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# To run this Streamlit app, save this code in a file named `app.py` and run `streamlit run app.py` in your terminal.
