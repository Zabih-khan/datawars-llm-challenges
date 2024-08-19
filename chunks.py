import argparse
import json
import os
from typing import List, Dict

def load_json(file_path: str) -> Dict:
    """Loads JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data: List[Dict], output_path: str):
    """Saves data to a JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def chunk_text(text: str, chunk_size: int, overlap: int) -> List[Dict]:
    """Chunks text into smaller pieces of chunk_size with overlap."""
    words = text.split()
    chunks = []
    start = 0
    chunk_id = 0

    while start < len(words):
        # Define chunk boundaries
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        
        # Join chunk words and create a chunk dict
        chunk_text = " ".join(chunk_words)
        chunks.append({
            "chunk_id": f"chunk_{chunk_id}",
            "text": chunk_text
        })
        
        chunk_id += 1
        # Move the start forward with overlap
        start = end - overlap if end < len(words) else end

    return chunks

def process_videos_folder(videos_folder: str, chunk_size: int, overlap: int):
    """Processes all subfolders in the videos folder."""
    for folder in os.listdir(videos_folder):
        folder_path = os.path.join(videos_folder, folder)
        
        if os.path.isdir(folder_path):
            transcript_file = os.path.join(folder_path, 'transcript.json')
            metadata_file = os.path.join(folder_path, 'metadata.json')
            
            if os.path.exists(transcript_file) and os.path.exists(metadata_file):
                print(f"Processing {folder}...")

                try:
                    # Load transcript and metadata
                    transcript_data = load_json(transcript_file)
                    metadata_data = load_json(metadata_file)
                    
                    # Check the structure of transcript_data
                    if ('results' in transcript_data and
                        'channels' in transcript_data['results'] and
                        isinstance(transcript_data['results']['channels'], list) and
                        len(transcript_data['results']['channels']) > 0 and
                        'alternatives' in transcript_data['results']['channels'][0] and
                        isinstance(transcript_data['results']['channels'][0]['alternatives'], list) and
                        len(transcript_data['results']['channels'][0]['alternatives']) > 0):
                        
                        # Extract transcript text
                        transcript_text = " ".join([alt['transcript'] for alt in transcript_data['results']['channels'][0]['alternatives']])
                        
                        # Chunk the transcript text
                        chunks = chunk_text(transcript_text, chunk_size, overlap)
                        
                        # Add additional metadata if needed
                        for chunk in chunks:
                            chunk.update({
                                "video_title": metadata_data.get("title", "Unknown Video"),
                                "video_id": metadata_data.get("video_id", "Unknown ID")
                            })
                        
                        # Define the output file
                        output_file = os.path.join(folder_path, 'chunks.json')
                        
                        # Save the chunks to output JSON
                        save_json(chunks, output_file)

                        print(f"Chunks saved to {output_file}")
                    else:
                        print(f"Unexpected structure in {transcript_file}: {transcript_data}")
                
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in {transcript_file}: {e}")
                except Exception as e:
                    print(f"Error processing {folder}: {e}")
            else:
                print(f"Skipping {folder} - transcript or metadata file missing.")

def process_playlists_folder(playlists_folder: str):
    """Processes metadata files in the playlists folder."""
    for folder in os.listdir(playlists_folder):
        folder_path = os.path.join(playlists_folder, folder)
        
        if os.path.isdir(folder_path):
            metadata_file = os.path.join(folder_path, 'metadata.json')
            
            if os.path.exists(metadata_file):
                print(f"Processing {folder}...")

                try:
                    # Load metadata
                    metadata_data = load_json(metadata_file)

                    # Save metadata to a new file (just an example action)
                    output_file = os.path.join(folder_path, 'processed_metadata.json')
                    save_json(metadata_data, output_file)

                    print(f"Processed metadata saved to {output_file}")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in {metadata_file}: {e}")
                except Exception as e:
                    print(f"Error processing {folder}: {e}")
            else:
                print(f"Skipping {folder} - metadata file missing.")

# Define folders and parameters
base_folder = r'E:\ML and Data Science work\Challenge\datawars-llm-challenges\transcripts'
chunk_size = 512
overlap = 100

# Define folders
playlists_folder = os.path.join(base_folder, 'playlists')
videos_folder = os.path.join(base_folder, 'videos')

# Verify that the folders exist
if not os.path.exists(playlists_folder):
    print(f"Error: The playlists folder does not exist: {playlists_folder}")
else:
    print(f"Playlists folder path is valid: {playlists_folder}")

if not os.path.exists(videos_folder):
    print(f"Error: The videos folder does not exist: {videos_folder}")
else:
    print(f"Videos folder path is valid: {videos_folder}")

# Process playlists and videos folders if paths are correct
if os.path.exists(playlists_folder):
    process_playlists_folder(playlists_folder)
    
if os.path.exists(videos_folder):
    process_videos_folder(videos_folder, chunk_size, overlap)