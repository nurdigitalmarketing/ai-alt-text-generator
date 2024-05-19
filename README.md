
# AI Alt Text Generator

AI Alt Text Generator is a web application built with Streamlit that allows you to upload multiple images, select the language for the alt text, and generate HTML code with the alt text. The results can be exported to an Excel file, making it ideal for enhancing image accessibility on websites.

## Features

- Upload multiple images
- Select the language for the alt text
- Generate HTML code with alt text for each image
- Export results to an Excel file

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/ai-alt-text-generator.git
   cd ai-alt-text-generator
   ```

2. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```sh
   streamlit run streamlit_app.py
   ```

2. Open your web browser and go to `http://localhost:8501`.

3. Follow the instructions on the web interface:
   - Enter your API key from [AltText.ai](https://alttext.ai/account/api_keys).
   - Select the language for the alt text.
   - Upload images from your device.
   - Generate the alt text and export the results to an Excel file.

## Dependencies

- [Streamlit](https://streamlit.io)
- [Requests](https://pypi.org/project/requests/)
- [Pillow](https://pypi.org/project/Pillow/)
- [Pandas](https://pypi.org/project/pandas/)
- [Streamlit Elements](https://pypi.org/project/streamlit-elements/)

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b my-feature-branch`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin my-feature-branch`
5. Open a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgments

This application relies on the excellent [AltText.ai](https://alttext.ai) API for generating alt text.
