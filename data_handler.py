from dotenv import load_dotenv
import os

from PyPDF2 import PdfReader
from docx import Document

from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
# from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
import openai
# from langchain.embeddings.openai import OpenAIEmbeddings

load_dotenv()

pinecone_key = os.getenv('PINECONE_API_TOKEN')
proxy_key = os.getenv('OPENAI_PROXY_KEY')
base_url = os.getenv('BASE_URL')

# Set the proxy API configuration
openai.api_base = base_url
openai.api_key = proxy_key

# set up an exisiting vector store with the index name 'finance'
pc = Pinecone(api_key=pinecone_key)
index = pc.Index('finance')

# print(index.describe_index_stats())

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


# Function to Extract Text from Uploaded DOCX
def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text = " ".join([paragraph.text for paragraph in doc.paragraphs])
    return text


def generate_embedding(text):
  response = openai.Embedding.create(
      model="text-embedding-ada-002",
      input=text
  )
  return response['data'][0]['embedding']


# Function to search for documents in Pinecone
def search_documents(input_text, top_k=10):
    # Step 1: Generate embedding for the input text
    query_embedding = generate_embedding(input_text)

    # Step 2: Query Pinecone with the embedding
    search_results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True  # Include metadata to get document details
    )

    # Step 3: Process and return the search results
    documents = []
    for match in search_results['matches']:
        documents.append({
            "id": match['id'],
            "score": match['score'],
            "metadata": match['metadata']
        })

    return documents