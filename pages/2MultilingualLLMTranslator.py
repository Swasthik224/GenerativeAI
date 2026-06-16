import streamlit as st
from deep_translator import GoogleTranslator
from pypdf import PdfReader
from docx import Document
from PIL import Image
import pytesseract
import os
import shutil

if shutil.which("tesseract"):
    pass
else:
    possible_tesseract_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Users\manju\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
    ]
    for path in possible_tesseract_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break

st.title("Project 2: Multimodal Language Translator")
st.write("Convert raw text, images, PDFs, or Word documents into multiple languages seamlessly.")
st.divider()

@st.cache_resource
def get_translator_and_languages():
    base_translator = GoogleTranslator()
    supported_langs = base_translator.get_supported_languages(as_dict=True)
    formatted_options = {name.title(): code for name, code in supported_langs.items()}
    return base_translator, formatted_options

base_translator, lang_options = get_translator_and_languages()

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

def extract_text_from_image(file):
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    return text

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Input Source")

    input_mode = st.radio(
        "Choose Input Type:",
        ["Type Text Directly", "Upload a File (PDF, DOCX, Image)"],
        horizontal=True
    )

    source_lang_name = st.selectbox(
        "Detect/Select Source Language:",
        ["Auto-Detect"] + list(lang_options.keys()),
        index=0
    )

    extracted_text = ""

    if input_mode == "Type Text Directly":
        extracted_text = st.text_area(
            label="Type or paste text to translate:",
            placeholder="Enter your content here...",
            height=250
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload an Image, PDF, or Word Document:",
            type=["pdf", "docx", "png", "jpg", "jpeg"]
        )

        if uploaded_file:
            file_extension = uploaded_file.name.split(".")[-1].lower()

            with st.spinner("Extracting content from file..."):
                try:
                    if file_extension == "pdf":
                        extracted_text = extract_text_from_pdf(uploaded_file)
                    elif file_extension == "docx":
                        extracted_text = extract_text_from_docx(uploaded_file)
                    elif file_extension in ["png", "jpg", "jpeg"]:
                        st.image(uploaded_file, caption="Uploaded Document Preview", width=300)
                        extracted_text = extract_text_from_image(uploaded_file)

                    if extracted_text.strip():
                        st.success("Text extracted successfully!")
                        with st.expander("View Extracted Text Preview"):
                            st.code(extracted_text, language="text")
                    else:
                        st.warning("No readable text could be discovered inside this file.")

                except Exception as e:
                    st.error(f"File Processing Error: {str(e)}")

with col2:
    st.markdown("### Translated Output")

    default_index = list(lang_options.keys()).index("Spanish") if "Spanish" in lang_options else 0

    target_lang_name = st.selectbox(
        "Select Target Language:",
        list(lang_options.keys()),
        index=default_index
    )

    st.write("Click below to process translations:")
    translate_button = st.button(
        "Translate Source",
        type="primary",
        use_container_width=True
    )

    st.markdown("---")

    if translate_button:
        if not extracted_text.strip():
            st.warning("No text content available to translate. Please type text or upload a valid file first.")
        else:
            with st.spinner("Processing translations..."):
                try:
                    target_code = lang_options[target_lang_name]

                    if source_lang_name == "Auto-Detect":
                        engine = GoogleTranslator(source="auto", target=target_code)
                        translated_text = engine.translate(extracted_text)
                        st.caption("Source Language: Auto-Detected")
                    else:
                        source_code = lang_options[source_lang_name]
                        engine = GoogleTranslator(source=source_code, target=target_code)
                        translated_text = engine.translate(extracted_text)

                    st.success("Translation Complete!")
                    st.info(translated_text)

                except Exception as e:
                    st.error(f"Translation System Error: {str(e)}")
                    st.info(
                        "Hint: Ensure you are connected to the internet so the app can reach the Translation servers."
                    )
