import os
import json
# from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from langchain_google_genai import GoogleGenerativeAIEmbeddings

google_api_key = "AIzaSyB8VwPGA08UUPd0ayNPCpHjJhIRxU6l_tI"

# Define the paths and load chunk data
chunks_dir = "E:\\ML and Data Science work\\Challenge\\datawars-llm-challenges\\Chunks"
combined_chunks_file = "combined_chunks.json"

# Function to combine chunks into a single JSON file (if needed)
def combine_chunks(chunks_dir):
    combined_chunks = []
    for folder_name in os.listdir(chunks_dir):
        folder_path = os.path.join(chunks_dir, folder_name)
        for file_name in os.listdir(folder_path):
            if file_name.startswith('chunked_') and file_name.endswith('.json'):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r') as file:
                    chunks = json.load(file)
                    combined_chunks.extend(chunks)
    return combined_chunks

# Combine chunks and save them to a file
combined_chunks = combine_chunks(chunks_dir)
with open(combined_chunks_file, "w") as outfile:
    json.dump(combined_chunks, outfile, indent=4)

# Load combined chunks
with open(combined_chunks_file, "r") as file:
    combined_chunks = json.load(file)

# Initialize the OpenAI embeddings model
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)

# Generate embeddings and store them in Chroma vector store
texts = [chunk['text'] for chunk in combined_chunks]
metadata = [{"chunk_id": chunk["chunk_id"]} for chunk in combined_chunks]

# Create and persist vector store
vector_store = Chroma.from_texts(texts, embeddings, metadatas=metadata, persist_directory="chroma_db")
vector_store.persist()

# Query the vector store for relevant chunks
query = "How can I group DataFrames in Pandas?"
results = vector_store.similarity_search(query, k=3)  # Get top 3 relevant chunks

# Print the results
for result in results:
    print(f"Chunk ID: {result.metadata['chunk_id']}")
    print(f"Text: {result.page_content}")
    print("\n")
