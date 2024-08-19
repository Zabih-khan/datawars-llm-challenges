import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

google_api_key = "AIzaSyB8VwPGA08UUPd0ayNPCpHjJhIRxU6l_tI"

def load_transcript(transcript_file):
    with open(transcript_file, 'r') as file:
        data = json.load(file)
    
    transcript_text = ""
    for channel in data['results']['channels']:
        for alternative in channel['alternatives']:
            transcript_text += alternative['transcript'] + " "
    
    return {
        "text": transcript_text.strip(),
        "video_id": data['metadata']['sha256']
    }

def chunk_transcript(transcript, max_chunk_size=500, overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=max_chunk_size, chunk_overlap=overlap)
    chunks = text_splitter.split_text(transcript['text'])
    
    chunked_data = []
    for i, chunk in enumerate(chunks):
        chunked_data.append({
            "chunk_id": f"{transcript['video_id']}_{i}",
            "text": chunk
        })
    return chunked_data

def save_chunks_to_file(chunked_data, output_file):
    with open(output_file, 'w') as file:
        json.dump(chunked_data, file, indent=4)

def process_all_transcripts(videos_dir, output_file, chunks_file, max_chunk_size=500, overlap=50):
    all_documents = []
    all_chunked_data = []
    
    for video_folder in os.listdir(videos_dir):
        video_path = os.path.join(videos_dir, video_folder)
        if os.path.isdir(video_path):
            transcript_path = os.path.join(video_path, "transcript.json")
            transcript = load_transcript(transcript_path)
            chunked_transcript = chunk_transcript(transcript, max_chunk_size, overlap)
            all_chunked_data.extend(chunked_transcript)
            
            documents = [Document(page_content=chunk['text'], metadata={"chunk_id": chunk["chunk_id"]}) for chunk in chunked_transcript]
            all_documents.extend(documents)
    
    # Save chunked data to JSON file
    save_chunks_to_file(all_chunked_data, chunks_file)
    
    # Create FAISS vector store from all documents
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)
    vector_store = FAISS.from_documents(all_documents, embedding_model)
    vector_store.save_local(output_file)

def create_strategy_document(strategy_file):
    strategy_text = """
# Chunking Strategy

## Strategy Overview
For this challenge, the transcript text is chunked using a length-based strategy. We use a maximum chunk size of 500 characters with an overlap of 50 characters to ensure that context is preserved across chunks.

## Chunking Strategy
- **Chunk Size**: 500 characters
- **Overlap**: 50 characters

## Tools and Frameworks
- **Text Chunking**: LangChain's RecursiveCharacterTextSplitter
- **Vector Store**: FAISS from LangChain Community

## Challenges and Considerations
- **Chunk Size**: A smaller chunk size allows for more precise retrieval but increases the number of chunks and storage requirements.
- **Overlap**: Ensures that context is maintained across chunks, which helps in better retrieval accuracy but also increases the number of tokens processed.
"""
    with open(strategy_file, 'w') as file:
        file.write(strategy_text)

# Specify your directory and output files here
videos_dir = "transcripts/videos/"
output_file = "combined_faiss_index"
chunks_file = "chunked_transcripts.json"

# Run processing
process_all_transcripts(videos_dir, output_file, chunks_file)
create_strategy_document("chunking_strategy.md")
