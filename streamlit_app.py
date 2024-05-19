import streamlit as st
import requests
import openai
import base64
from PIL import Image
import io
import logging
import pandas as pd

# Setup logging
logging.basicConfig(level=logging.INFO)

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

# API key input for AltText.ai
ALT_TEXT_API_KEY = st.text_input("Inserisci la tua chiave API da [AltText.ai](https://alttext.ai/account/api_keys):", type="password")
# API key input for OpenAI
OPENAI_API_KEY = st.text_input("Inserisci la tua chiave API di OpenAI:", type="password")

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

# API selection
api_options = ["AltText.ai", "OpenAI"]
selected_api = st.selectbox("Seleziona l'API per generare l'alt text:", api_options)

def generate_clip_description(image):
    # Placeholder function for CLIP model inference
    return "breve descrizione dell'immagine"

def generate_alt_text_openai(description, api_key):
    client = openai.OpenAI(api_key=api_key)
    
    prompt = f"Generate a detailed alt text for the following image description: {description}"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    
    alt_text = response.choices[0].message.content.strip()
    logging.info(f"Response from OpenAI API: {response}")
    
    return alt_text

# Prepare data for DataFrame
results = []

if (ALT_TEXT_API_KEY or OPENAI_API_KEY) and uploaded_files:
    st.write(f"Generating alt text in {selected_language} using {selected_api} API...")
    for uploaded_file in uploaded_files:
        if selected_api == "AltText.ai":
            alt_text_response = generate_alt_text_alttextai(uploaded_file, ALT_TEXT_API_KEY, languages[selected_language])
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
        elif selected_api == "OpenAI":
            img = Image.open(uploaded_file)
            clip_description = generate_clip_description(img)
            alt_text = generate_alt_text_openai(clip_description, OPENAI_API_KEY)
            html_code = f'<img src="{uploaded_file.name}" alt="{alt_text}">'
            results.append([uploaded_file.name, alt_text, html_code])

# Display results in a table
if results:
    df = pd.DataFrame(results, columns=["Image Name", "Alt Text", "HTML Code"])
    st.write(df)

    if st.button("Export to Excel"):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='AltText')
            writer.save()
        st.download_button(label="Download Excel file", data=output.getvalue(), file_name="alt_text_results.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# To run this Streamlit app, save this code in a file named `app.py` and run `streamlit run app.py` in your terminal.
