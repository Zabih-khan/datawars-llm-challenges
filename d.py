import os
import json
import argparse
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_transcript(transcript_file):
    with open(transcript_file, 'r') as file:
        data = json.load(file)
    
    transcript_text = ""
    for channel in data['results']['channels']:
        for alternative in channel['alternatives']:
            transcript_text += alternative['transcript'] + " "
    
    metadata = {
        "video_id": data['metadata']['sha256'],
        "title": data['metadata'].get('title', 'Unknown Title'),
    }
    
    return {
        "text": transcript_text.strip(),
        "metadata": metadata
    }

def chunk_transcript(transcript, max_chunk_size=500, overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=max_chunk_size, chunk_overlap=overlap)
    chunks = text_splitter.split_text(transcript['text'])
    
    chunked_data = []
    for i, chunk in enumerate(chunks):
        chunked_data.append({
            "chunk_id": f"{transcript['metadata']['video_id']}_{i}",
            "text": chunk
        })
    return chunked_data

def save_chunks_to_file(chunked_data, output_file):
    output_dir = os.path.join("E:\\ML and Data Science work\\Challenge\\datawars-llm-challenges\\Chunks", chunked_data[0]["chunk_id"].split('_')[0])
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file_path = os.path.join(output_dir, os.path.basename(output_file))
    with open(output_file_path, 'w') as file:
        json.dump(chunked_data, file, indent=4)
    
    print(f"Chunks saved to: {output_file_path}")

def main():
    parser = argparse.ArgumentParser(description="Chunk video transcripts with metadata")
    parser.add_argument('--videos_dir', required=True, help="Path to the directory containing video folders")
    parser.add_argument('--max_chunk_size', type=int, default=500, help="Maximum size of a chunk")
    parser.add_argument('--overlap', type=int, default=50, help="Number of overlapping characters between chunks")

    args = parser.parse_args()

    for video_folder in os.listdir(args.videos_dir):
        video_path = os.path.join(args.videos_dir, video_folder)
        transcript_path = os.path.join(video_path, "transcript.json")
        
        if os.path.isfile(transcript_path):
            transcript = load_transcript(transcript_path)
            chunked_data = chunk_transcript(transcript, args.max_chunk_size, args.overlap)
            
            output_filename = f"chunked_{video_folder}.json"
            save_chunks_to_file(chunked_data, output_filename)

if __name__ == "__main__":
    main()

# Command to run the script:
# python d.py --videos_dir "E:\ML and Data Science work\Challenge\datawars-llm-challenges\transcripts\videos" --max_chunk_size 500 --overlap 50
