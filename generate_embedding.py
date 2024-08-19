from langchain.vectorstores import Chroma
import json

from langchain_google_genai import GoogleGenerativeAIEmbeddings

google_api_key = "AIzaSyB8VwPGA08UUPd0ayNPCpHjJhIRxU6l_tI"
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)



# Load the combined chunks
with open("combined_chunks.json", "r") as file:
    combined_chunks = json.load(file)

# Prepare the text data for embedding
texts = [chunk['text'] for chunk in combined_chunks]
metadata = [{"chunk_id": chunk["chunk_id"]} for chunk in combined_chunks]

# Generate and store embeddings in Chroma
vector_store = Chroma.from_texts(texts, embeddings, metadatas=metadata, persist_directory="chroma_db")
vector_store.persist()
