from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List 
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
def extract_data(data):
    loader=DirectoryLoader(
        data,
        glob='*.pdf',
        loader_cls=PyPDFLoader
    )
    file=loader.load()
    return file

def minimal_docs(docs: List[Document]):
    min_docs:list[Document]=[]
    for doc in docs:
        src= doc.metadata.get('source')
        min_docs.append(
            Document (
            page_content=doc.page_content,
            metadata={'sorce':src}
            )
        )
    return min_docs   

def text_split(minmal_docss):
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
    )
    texts_chunks=text_splitter.split_documents(minmal_docss)
    return texts_chunks 

def download_embeddings():
    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
    
    return embeddings

    
