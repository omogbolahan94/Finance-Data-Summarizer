import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.vectorstores import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
import pinecone
from PyPDF2 import PdfReader
from docx import Document
from fpdf import FPDF
from data_handler import extract_text_from_pdf, extract_text_from_text

# Title of the Streamlit App
st.title("Financial Data Summarizer with RAG")

# Upload the Financial Document
uploaded_file = st.file_uploader("Upload a financial document (.pdf or .docx):", type=["pdf", "docx"])

# Extract text from the uploaded file
if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        document_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        document_text = extract_text_from_docx(uploaded_file)
    
    # split the document
    text_splitter_recursive = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    company_data_chunks = text_splitter_recursive.split_text(document_text)
    
    # Embed the document into Pinecone
    for data in company_data_chunks:
        embedding = generate_embedding(data)
        index.upsert([
            {"id": f"doc-{hash(data)}", "values": embedding, "metadata": {"text": data}}
        ])
    
    st.success("Document successfully embedded into the vector database!")

    