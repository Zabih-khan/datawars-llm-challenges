# DataWars LLM Challenges

This repository contains the code and instructions for the DataWars LLM Candidate Challenge, which involves chunking video transcripts and creating an agent to assist students with queries about Pandas and Matplotlib tutorials.

## Setup

1. **Install Dependencies**

   First, install all required dependencies. Ensure you have `pip` installed and use the following command:

   ```bash
   pip install -r requirements.txt
   ```


2. **Create Chunks from Video Transcripts**

    After installing the dependencies, you need to run the chunks.py script to process the video transcripts and generate text chunks.

    Use the following command in your terminal to run the script:

      ```bash
   python chunks.py --output chunks.json
   ```
   The output will be saved in the chunks_output folder.



3. **Run the Agent**

    Once the chunks are created, you can run the agent.py script to start the agent that assists with queries.

    Use the following command to run the agent:
      ```bash
   python agent.py
   ```




