# Generative AI Portfolio Dashboard

An interactive multi-page Streamlit application acting as a central dashboard for two standalone micro-applications: an SOP RAG System and a Multilingual Language Translator.

---

## 🚀 Micro-Applications

### 1. SOP RAG System
An authenticated semantic search engine engineered to query internal company documentation.
* **Database & Framework:** ChromaDB and Sentence Transformers (`all-MiniLM-L6-v2`)
* **Role-Based Access Control:** Differentiated dynamic dashboard views for Admins, Employees, and Students.
* **Document Processing:** Automated chunking and embedding pipeline for user-uploaded PDF manuals.

### 2. Multilingual Language Translator
A multimodal processing tool that extracts and translates text content across dozens of languages.
* **Translation Engine:** Driven by the Google Translation API framework via `deep-translator`.
* **Multimodal Extraction:** Supports direct text inputs as well as automated text extraction from uploaded PDF, Word (`.docx`), and Image files using PyTesseract OCR.

---

## 📂 Project Structure

```text
GenerativeAI/
├── app.py                     # Main portfolio dashboard landing page
├── packages.txt               # System-level dependencies for Linux/Cloud hosting
├── requirements.txt           # Python package dependencies
├── pages/
│   ├── 1_SOP_RAG.py           # Authenticated Vector Search applicati



```
Local Installation
Prerequisites
Python 3.9 or higher

Tesseract OCR installed on your local operating system

Setup Steps
Clone this repository to your local machine:

Bash
   git clone https://github.com/Swasthik224/GenerativeAI.git
   cd generative-ai-portfolio
Create and activate a virtual environment:

Bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
Install the required Python packages:

Bash
   pip install -r requirements.txt
Launch the application dashboard:

Bash
   streamlit run app.py



on
│   └── 2MultilingualLLMTranslator.py # Multimodal translation system
└── chroma_db/                 # Local directory for persistent vector storage
