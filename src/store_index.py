from dotenv import load_dotenv
import os 
from src.helper import extract_data, minimal_docs, text_split, download_embeddings
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore

load_dotenv()

PINECONE_API_KEY=os.getenv('PINECONE_API_KEY') 


os.environ['PINECONE_API_KEY']=PINECONE_API_KEY


extracted_data=extract_data('data')
minmal_docss=minimal_docs(extracted_data)
texts_chunk= text_split(minmal_docss)
embeddings =download_embeddings()

PINECONE_API_KEY=PINECONE_API_KEY
pc=Pinecone(PINECONE_API_KEY)


index_name ="medicalbot"
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric='cosine',
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )
index=pc.Index(index_name)    

docsearch =PineconeVectorStore.from_documents(
    documents=texts_chunk,
    embedding=embeddings,
    index_name=index_name
)

