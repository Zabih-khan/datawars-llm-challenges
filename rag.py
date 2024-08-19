import json
import os
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
print("This step is working")

def process_video(video_dir, output_folder):
    print(f"Processing video in directory: {video_dir}")
    """Processes a single video's transcript and metadata."""
    transcript_path = os.path.join(video_dir, "transcript.json")
    metadata_path = os.path.join(video_dir, "metadata.json")

    # Load transcript and metadata
    with open(transcript_path, 'r') as f:
        transcript_data = json.load(f)
        # Extract transcript text
        text = transcript_data['results']['channels'][0]['alternatives'][0]['transcript']

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
        # Get video metadata such as timestamps, titles, etc.
        video_duration = metadata.get('duration', 'unknown')

    # Create chunks with metadata
    chunks = create_chunks(text, video_duration)

    # Save chunks to a folder and also combine them into one JSON
    save_chunks(chunks, video_dir, output_folder)

def create_chunks(text: str, video_duration: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, str]]:
    """Creates chunks of the text with specified size and overlap, preserving semantic context."""
    print("Creating chunks.............")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    chunks = text_splitter.split_text(text)
    
    # Annotate chunks with video metadata (e.g., duration, potential start time, etc.)
    annotated_chunks = []
    for i, chunk in enumerate(chunks):
        chunk_metadata = {
            "chunk_id": f"chunk_{i+1}",
            "text": chunk,
            "video_duration": video_duration,
            "estimated_start_time": estimate_chunk_start_time(i, len(chunks), video_duration)
        }
        annotated_chunks.append(chunk_metadata)
    
    return annotated_chunks

def estimate_chunk_start_time(chunk_index, total_chunks, video_duration):
    """Estimate the start time of the chunk within the video based on its index."""
    # A simple proportional estimation (better approaches can be added based on specific metadata)
    if video_duration == 'unknown':
        return 'unknown'
    
    duration_in_seconds = float(video_duration)
    chunk_start_time = (chunk_index / total_chunks) * duration_in_seconds
    return f"{int(chunk_start_time // 60)}:{int(chunk_start_time % 60):02d}"

def save_chunks(chunks: List[Dict[str, str]], video_dir: str, output_folder: str):
    """Saves the chunks to a separate folder and combines all into one JSON file."""
    # Create folder to store individual chunk files
    chunks_dir = os.path.join(output_folder, "chunks")
    os.makedirs(chunks_dir, exist_ok=True)
    
    # Save each chunk as a separate file in the chunks folder
    for chunk in chunks:
        chunk_file = os.path.join(chunks_dir, f"{chunk['chunk_id']}.json")
        with open(chunk_file, 'w') as f:
            json.dump({
                "chunk_id": chunk['chunk_id'],
                "text": chunk['text'],
                "estimated_start_time": chunk['estimated_start_time']
            }, f, indent=4)

    # Combine all chunks into a single JSON file
    combined_chunks_file = os.path.join(output_folder, "combined_chunks.json")
    with open(combined_chunks_file, 'a') as combined_file:
        combined_file.write(json.dumps(chunks, indent=4))

def main():
    """Main function to orchestrate the entire process."""
    videos_dir = r"E:\ML and Data Science work\Challenge\datawars-llm-challenges\transcripts\videos"
    output_folder = r"E:\ML and Data Science work\Challenge\datawars-llm-challenges\processed_chunks"
    os.makedirs(output_folder, exist_ok=True)

    print("Processing videos.............")
    combined_chunks = []

    for video_dir in os.listdir(videos_dir):
        video_path = os.path.join(videos_dir, video_dir)
        if os.path.isdir(video_path):
            process_video(video_path, output_folder)
            print(f"Finished processing video directory: {video_path}")

if __name__ == "__main__":
    main()
