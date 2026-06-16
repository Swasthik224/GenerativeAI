import streamlit as st

# Global configuration applied across ALL pages
st.set_page_config(
    page_title="My AI Portfolio",
    page_icon="🤖",
    layout="wide"
)

# Custom Styles
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>🤖 Generative AI Portfolio Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Welcome! Use the sidebar navigation or the action cards below to launch independent micro-applications.</p>", unsafe_allow_html=True)
st.divider()

# Grid Layout for Portfolio Summary
col1, col2= st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("### 📄 Project 1: SOP RAG System")
        st.write("An authenticated semantic search engine built with ChromaDB and Sentence Transformers to query company documentation.")
        st.page_link("pages/1_SOP_RAG.py", label="Launch SOP Application", icon="🚀")

with col2:
    with st.container(border=True):
        st.markdown("### 🌐 Project 2: Multilingual Translator")
        st.write("Convert your text or SOP prompts into multiple languages seamlessly using the Google Translation Engine.")
        st.page_link("pages/2MultilingualLLMTranslator.py", label="Launch Translator Application", icon="🌐")

