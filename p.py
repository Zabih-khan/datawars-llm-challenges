import os
import json
import argparse
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import openai
from langchain_chroma import Chroma

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_transcript(transcript_path):
    """Load transcript from JSON file."""
    with open(transcript_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['results']['channels'][0]['alternatives'][0]['transcript']

def chunk_transcript(transcript, min_chunk_size=500, max_chunk_size=1000):
    """Chunk transcript text using RecursiveCharacterTextSplitter."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=max_chunk_size, chunk_overlap=50)
    chunks = splitter.split_text(transcript)
    
    # Structure the chunk data for JSON
    chunk_data = [{"chunk_id": f"{i+1}", "text": chunk} for i, chunk in enumerate(chunks)]
    return chunk_data

def process_videos(videos_dir, output_file="chunks.json"):
    """Process all videos in a directory and save chunks to a JSON file."""
    all_chunks = []

    for video_folder in os.listdir(videos_dir):
        video_path = os.path.join(videos_dir, video_folder)
        metadata_path = os.path.join(video_path, "metadata.json")
        transcript_path = os.path.join(video_path, "transcript.json")

        if os.path.exists(metadata_path) and os.path.exists(transcript_path):
            with open(metadata_path, 'r', encoding='utf-8') as file:
                metadata = json.load(file)
            transcript = load_transcript(transcript_path)

            chunks = chunk_transcript(transcript)
            all_chunks.extend(chunks)
        else:
            print(f"Missing metadata or transcript for {video_folder}")

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(all_chunks, outfile, ensure_ascii=False, indent=2)

def get_openai_embeddings(texts):
    """Generate embeddings for a list of texts using OpenAI's API."""
    openai_embeddings = OpenAIEmbeddings()
    embeddings = openai_embeddings.embed_documents(texts)
    return embeddings

def create_embeddings_from_chunks(chunk_file):
    """Create embeddings from chunks and store in a vector database."""
    with open(chunk_file, 'r', encoding='utf-8') as file:
        chunks = json.load(file)
    
    texts = [chunk['text'] for chunk in chunks]
    print(texts)
    # embeddings = get_openai_embeddings(texts)

    # # Store embeddings in a vector database
    # db = Chroma.from_documents(chunks, embeddings)


if __name__ == "__main__":
    videos_directory = "transcripts/videos"
    process_videos(videos_directory)
    create_embeddings_from_chunks("chunks.json")
