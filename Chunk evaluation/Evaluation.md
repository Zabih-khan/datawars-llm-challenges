# Chunking Strategy for DataWars LLM Challenge

## Overview

This document outlines the strategy and implementation details for chunking video transcripts as part of the DataWars LLM Candidate Challenge. The goal is to preprocess video transcripts into manageable chunks that can be efficiently used by a Retrieval-Augmented Generation (RAG) model for answering user queries.

## Chunking Transcripts Strategy

- **Text Splitter**: We use `RecursiveCharacterTextSplitter` from LangChain to split the transcript text.
- **Parameters**:
  - `max_chunk_size`: The maximum length of each chunk, set to 800 characters.
  - `overlap`: The number of overlapping characters between chunks, set to 100 characters.
- **Separators**: Chunks are split at punctuation marks and new lines (`.`, `,`, `\n`, `\n\n`).

## Why This Strategy Works

**Chunk Size and Overlap**: Setting the chunk size to 1000 characters makes it easier for the model to process the information. The overlap of 200 characters ensures that important information is not lost between chunks.

### Why I Chose Length-Based and Sentence Boundary Chunking

**Simplicity and Efficiency**: Using a fixed chunk size is simple and helps control the number of tokens (words and symbols) the model processes. Breaking chunks at sentence boundaries makes the text easier to read and understand.

**Maximum/Minimum Chunk Size**: A chunk size of 1000 characters gives enough context for the model to understand while staying within limits. The 200-character overlap helps keep the flow of information between chunks.


## Evaluation Metrics Results

### RAGAS Evaluation Technique

The **RAGAS (Retrieval-Augmented Generation Answer Scoring)** technique is used to evaluate how well the system performs. It combines different scores (retrieval and generation) into one final score, making sure both parts are balanced.

### Retrieval Metrics:

- **Context Precision (0.9977)**: This measures how relevant the information retrieved is. The score is very high, meaning the system retrieves the right information almost every time.
- **Context Recall (0.7999)**: This shows how much of the needed information is retrieved. It's a good score.

### Generation Metrics:

- **Faithfulness (0.9449)**: This measures how accurate the generated answer is compared to the given information. The system does well in providing correct information.
- **Answer Relevancy (0.8983)**: This checks if the answer matches the question. The score is good.
- **Answer Similarity (0.9715)**: This checks how similar the answer is to a reference answer. The score is very high, meaning the answers are closely related to the ideal response.

Screenshots show how the system answers a question like "How can I group a DataFrame in Pandas?" The system retrieves the correct chunks from the video transcript. You can compare the results with the actual transcript at the 14:50 mark.


![Original Content](./original_content.png)
![Chunk Output](./chunk_output.png)

## Conclusion

The strategy of chunking by character length with overlap strikes a balance between readability and efficient retrieval. Using `RecursiveCharacterTextSplitter`, we ensure chunks are clear and complete, with important information not being cut off. The overlap helps maintain key details across chunks, making the system capable of providing accurate and useful responses. This method is effective for processing and managing video transcript data in the challenge.
