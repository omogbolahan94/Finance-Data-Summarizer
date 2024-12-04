from dotenv import load_dotenv
import os

from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
# from langchain.embeddings.openai import OpenAIEmbeddings

load_dotenv()

secret_key = os.getenv('PINECONE_API_TOKEN')

# set up an exisiting vector store with the index name 'finance'
pc = Pinecone(api_key=pinecone_key)
index = pc.Index('finance')

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