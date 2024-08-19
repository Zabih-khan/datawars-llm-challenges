import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

def load_transcript(transcript_file):
    with open(transcript_file, 'r') as file:
        data = json.load(file)
    
    transcript_text = ""
    # Concatenate all transcript text
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

def save_chunked_data(chunked_data, output_file):
    with open(output_file, 'w') as file:
        json.dump(chunked_data, file, indent=2)

def process_video_folder(video_path):
    transcript_path = os.path.join(video_path, "transcript.json")
    
    transcript = load_transcript(transcript_path)
    chunked_transcript = chunk_transcript(transcript)
    
    # Save the chunked data in JSON format
    output_chunks_file = os.path.join(video_path, "chunked_transcript.json")
    save_chunked_data(chunked_transcript, output_chunks_file)

    # Optional: Create FAISS index if needed
    documents = [Document(page_content=chunk['text'], metadata={"chunk_id": chunk["chunk_id"]}) for chunk in chunked_transcript]
    vector_store = FAISS.from_documents(documents, OpenAIEmbeddings())
    index_file = os.path.join(video_path, "faiss_index")
    vector_store.save_local(index_file)

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

if __name__ == "__main__":
    videos_dir = "transcripts/videos/"
    
    for video_folder in os.listdir(videos_dir):
        video_path = os.path.join(videos_dir, video_folder)
        if os.path.isdir(video_path):
            print(f"Processing {video_folder}...")
            process_video_folder(video_path)
    
    # Create a strategy document in the root directory
    create_strategy_document("chunking_strategy.md")
