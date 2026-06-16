import streamlit as st
import chromadb
from PyPDF2 import PdfReader
import sys
import os
import traceback

print("STARTING SOP_RAG")
from sentence_transformers import SentenceTransformer

USER_REGISTRY = {
    "admin": {"password": "password123", "role": "Admin"},
    "employee": {"password": "emp123", "role": "Employee"},
    "student": {"password": "stud123", "role": "Student"}
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "username" not in st.session_state:
    st.session_state.username = None

print("STARTING SOP_RAG1")

@st.cache_resource
def get_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource
def get_chroma_client():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(root_dir, "chroma_db")

    if not os.path.exists(db_path):
        os.makedirs(db_path)

    from chromadb.config import Settings

    return chromadb.PersistentClient(
        path=db_path,
        settings=Settings(anonymized_telemetry=False)
    )

print("STARTING SOP_RAG2")

def process_pdf(uploaded_file, chunk_size=500, overlap=50):
    reader = PdfReader(uploaded_file)
    chunks = []
    metadata = []

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()

        if not text:
            continue

        start = 0

        while start < len(text):
            chunk = text[start:start + chunk_size]
            chunks.append(chunk)
            metadata.append({"page": page_num + 1})
            start += chunk_size - overlap

    return chunks, metadata

print("STARTING SOP_RAG4")

def show_login_page():
    st.title("Project 1: Access Portal")
    st.write("Please sign in to access the isolated SOP RAG application.")

    with st.form("login_form"):
        username_input = st.text_input("Username").strip()
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Log In")

        if submit_button:
            username_lower = username_input.lower()

            if (
                username_lower in USER_REGISTRY and
                USER_REGISTRY[username_lower]["password"] == password
            ):
                st.session_state.logged_in = True
                st.session_state.user_role = USER_REGISTRY[username_lower]["role"]
                st.session_state.username = username_input

                st.success(
                    f"Verified! Loading dynamic {st.session_state.user_role} view..."
                )
                st.rerun()
            else:
                st.error("Invalid username or password.")

print("STARTING SOP_RAG5")

def show_rag_interface():
    st.write("DEBUG A - Entered RAG Interface")

    role = st.session_state.user_role

    col1, col2 = st.columns([4, 1])

    with col1:
        st.title("SOP Handbook Search Engine")
        st.caption(
            f"Authenticated Identity: {st.session_state.username} ({role} Privileges)"
        )

    with col2:
        if st.button("Log Out of SOP", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.session_state.username = None
            st.rerun()

    st.divider()

    st.write("DEBUG B - Loading SentenceTransformer")

    try:
        model = get_embedding_model()
        st.success("DEBUG C - SentenceTransformer Loaded Successfully")
    except Exception:
        st.error("MODEL LOADING ERROR")
        st.code(traceback.format_exc())
        st.stop()

    print("STARTING SOP_RAG6")

    st.write("DEBUG D - Loading ChromaDB")

    try:
        chroma_client = get_chroma_client()
        st.success("DEBUG E - ChromaDB Loaded Successfully")
    except Exception:
        st.error("CHROMADB ERROR")
        st.code(traceback.format_exc())
        st.stop()

    if role == "Admin":
        st.success("DEBUG F - Admin View Loaded")
        st.subheader("Vector Collection Builder")

        target_role = st.selectbox(
            "Select Target Audience for Document Configuration:",
            ["Employee", "Student"]
        )

        target_collection = f"handbook_{target_role.lower()}"

        uploaded_file = st.file_uploader(
            f"Upload fresh PDF document for {target_role}s",
            type="pdf"
        )

        if uploaded_file and st.button(
            f"Initialize and Index Fresh Database for {target_role}s"
        ):
            try:
                with st.spinner("Processing PDF..."):
                    try:
                        chroma_client.delete_collection(target_collection)
                    except:
                        pass

                    collection = chroma_client.create_collection(
                        target_collection
                    )

                    chunks, metadatas = process_pdf(uploaded_file)

                    st.write(f"DEBUG G - Created {len(chunks)} Chunks")

                    embeddings = model.encode(chunks).tolist()

                    st.write("DEBUG H - Embeddings Created")

                    ids = [str(i) for i in range(len(chunks))]

                    collection.add(
                        ids=ids,
                        documents=chunks,
                        embeddings=embeddings,
                        metadatas=metadatas
                    )

                    st.success("Database Created Successfully")

            except Exception:
                st.error("PDF PROCESSING ERROR")
                st.code(traceback.format_exc())

    else:
        st.success("DEBUG I - User View Loaded")

        collection_name = f"handbook_{role.lower()}"

        try:
            collection = chroma_client.get_collection(collection_name)

            st.success("DEBUG J - Collection Found")

            if collection.count() > 0:
                user_query = st.text_input("Search Handbook")

                if user_query:
                    st.write("DEBUG K - Running Query")

                    results = collection.query(
                        query_embeddings=[
                            model.encode(user_query).tolist()
                        ],
                        n_results=3
                    )

                    st.success("DEBUG L - Query Success")
                    st.write(results)

            else:
                st.warning("Collection Empty")

        except Exception:
            st.error("COLLECTION ERROR")
            st.code(traceback.format_exc())

if st.session_state.logged_in:
    show_rag_interface()
else:
    show_login_page()
