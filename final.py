import json
import os
import argparse
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_transcript(transcript_path):
    with open(transcript_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['results']['channels'][0]['alternatives'][0]['transcript']

def chunk_transcript(transcript, min_chunk_size=500, max_chunk_size=1000):
    splitter = RecursiveCharacterTextSplitter(chunk_size=max_chunk_size, chunk_overlap=50)
    chunks = splitter.split_text(transcript)
    
    # Structure the chunk data for JSON
    chunk_data = [{"chunk_id": f"{i+1}", "text": chunk} for i, chunk in enumerate(chunks)]
    return chunk_data

def process_video(transcript_path, metadata_path, output_file):
    transcript = load_transcript(transcript_path)
    chunks = chunk_transcript(transcript)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(chunks, outfile, ensure_ascii=False, indent=2)

if __name__ == "__main__":

    videos_dir = "transcripts/videos/"

    for video_folder in os.listdir(videos_dir):
        video_path = os.path.join(videos_dir, video_folder)
        metadata_path = os.path.join(video_path, "metadata.json")
        transcript_path = os.path.join(video_path, "transcript.json")


    process_video(transcript_path, metadata_path, "chunks.json")