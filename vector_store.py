from dotenv import load_dotenv
import os

from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
# from langchain.embeddings.openai import OpenAIEmbeddings

load_dotenv()

if __name__ == '__main__':
    secret_key = os.getenv('PINECONE_API_TOKEN')

    # set up an exisiting vector store with the index name 'finance'
    pc = Pinecone(api_key=pinecone_key)
    index = pc.Index('finance')

    # load the dataset
    loader = DirectoryLoader('/data', glob="./*.docx")
    data = loader.load()

    print(secret_key)