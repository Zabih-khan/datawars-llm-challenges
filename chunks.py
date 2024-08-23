import os
import json
import argparse
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_metadata(metadata_file):
    """Load and return metadata from a specified JSON file."""
    with open(metadata_file, 'r') as file:
        metadata = json.load(file)
    return metadata

def load_transcript(transcript_file, metadata):
    """Load transcript text and metadata from a JSON file."""
    with open(transcript_file, 'r') as file:
        data = json.load(file)
    
    transcript_text = " ".join(
        word_info['punctuated_word']
        for channel in data['results']['channels']
        for alternative in channel['alternatives']
        for word_info in alternative['words']
    )
    
    video_id = data['metadata']['sha256']
    title = metadata.get('title', 'Unknown Title')
    
    return {
        "text": transcript_text.strip(),
        "metadata": {"video_id": video_id, "title": title}
    }

def chunk_transcript(transcript, max_chunk_size, overlap):
    """Split the transcript text into chunks with a maximum size and overlap."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_chunk_size,
        chunk_overlap=overlap,
        length_function=len,
        separators=['.', ',', '\n', '\n\n'] 
    )
    chunks = text_splitter.split_text(transcript['text'])
    
    return [
        {"title": transcript['metadata']['title'], "text": chunk}
        for chunk in chunks
    ]

def save_chunks_to_file(combined_chunks, output_file):
    """Save the list of chunked data to a JSON file in a specified output folder."""
    output_folder = "chunks_output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_file_path = os.path.join(output_folder, output_file)
    
    with open(output_file_path, 'w') as file:
        json.dump(combined_chunks, file, indent=4)
    
    print(f"All chunks saved to: {output_file_path}")

def main():
    """Main function to process transcripts, chunk them, and save the results to a JSON file."""
    
    parser = argparse.ArgumentParser(description="Chunk video transcripts and save to a JSON file.")
    parser.add_argument("--output", type=str, required=True, help="Output file name for the combined chunks")
    
    args = parser.parse_args()
    
    current_directory = os.getcwd()
    videos_directory = os.path.join(current_directory, "transcripts", "videos")
    
    combined_chunks = []

    for video_folder in os.listdir(videos_directory):
        video_path = os.path.join(videos_directory, video_folder)
        transcript_path = os.path.join(video_path, "transcript.json")
        metadata_path = os.path.join(video_path, "metadata.json")
        
        if os.path.isfile(transcript_path) and os.path.isfile(metadata_path):
            metadata = load_metadata(metadata_path)
            transcript = load_transcript(transcript_path, metadata)
            chunked_data = chunk_transcript(transcript, max_chunk_size=1000, overlap=200)
            combined_chunks.extend(chunked_data)

    save_chunks_to_file(combined_chunks, args.output)

if __name__ == "__main__":
    main()
