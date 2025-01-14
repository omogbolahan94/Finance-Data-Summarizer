import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.vectorstores import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter, TokenTextSplitter
import pinecone
from fpdf import FPDF
from data_handler import extract_text_from_pdf, extract_text_from_docx, generate_embedding, search_documents, index
from summarizer import summarize_results
from web_crawler import get_financial_data
import save_document

# Title of the Streamlit App
st.title("Private Intel RAG")

# Collect the Company's Name
company_name = st.text_input("Enter the company's name:")

# Upload the Financial Document
uploaded_file = st.file_uploader("Upload a financial document (.pdf or .docx):", type=["pdf", "docx"])

# Extract text from the uploaded file
if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        document_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        document_text = extract_text_from_docx(uploaded_file)
    
    # split the document
    text_splitter_recursive = TokenTextSplitter(chunk_size=200, chunk_overlap=30)
    company_data_chunks = text_splitter_recursive.split_text(document_text)
    
    # Embed the document into Pinecone
    index.delete(delete_all=True)

    for data in company_data_chunks:
        embedding = generate_embedding(data)
        index.upsert([
            {"id": f"doc-{hash(data)}", "values": embedding, "metadata": {"text": data}}
        ])
    
    st.success("Document successfully embedded into the vector database!")


    # extract test from the prompt
    prompt = extract_text_from_docx('Prompt_template.docx')
    text_splitter = TokenTextSplitter(chunk_size=150, chunk_overlap=20)
    prompt_chunks = text_splitter.split_text(prompt)


    generated_prompt = " "

    for input_text in prompt_chunks:
        results = search_documents(input_text)
        for doc in results:
            generated_prompt += doc['metadata']['text']

        generated_prompt += '\n\n'

    # crawl data from the web
    finantial_data = None # get_financial_data()

    if finantial_data is None:
        summary = summarize_results(generated_prompt, company_name)
    else:
        summary = summarize_results(generated_prompt, company_name)

    save_document.save_summary(summary)