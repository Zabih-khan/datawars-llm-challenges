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

**Chunk Size and Overlap**: 800 characters is a typical sweet spot for LLM models to process. It keeps chunks small enough to avoid exceeding token limits but large enough to retain context. The overlap ensures that even if a relevant part of the text spans two chunks, both chunks contain enough information to remain useful for retrieval.

### Why I Chose Length-Based and Sentence Boundary Chunking

**Simplicity and Efficiency**: Using fixed chunk sizes is an efficient way to manage token costs and ensure each chunk fits within the LLM's token limits. Sentence boundary chunking provides a balance of coherence and ease of implementation.

**Maximum/Minimum Chunk Size**: A maximum chunk size of 800 characters strikes a good balance between providing enough context for retrieval while staying within typical LLM token limits. The overlap of 100 characters preserves context between chunks, preventing sentences from being cut off and preserving meaning.

## Evaluation Metrics Results

### RAGAS Evaluation Technique

The **RAGAS (Retrieval-Augmented Generation Answer Scoring)** technique is used to evaluate the system's performance. It calculates a **harmonic mean** of individual metric scores, ensuring a balanced assessment of both retrieval and generation quality.

### Retrieval Metrics:

- **Context Precision (0.9977)**: Measures how relevant the retrieved context is. Very high precision, meaning mostly relevant information is retrieved.
- **Context Recall (0.7999)**: Measures how much of the necessary information is retrieved. Good, but could be improved to capture more relevant content.

### Generation Metrics:

- **Faithfulness (0.9449)**: Measures how factually consistent the answer is with the context. Strong performance.
- **Answer Relevancy (0.8983)**: Measures how relevant the answer is to the question. Good, but room for fine-tuning.
- **Answer Correctness (0.7227)**: Measures how accurate the answer is. Needs improvement.
- **Answer Similarity (0.9715)**: Measures how similar the answer is to a reference answer. Very high similarity.

Screenshots demonstrate that when asking the question "How can I group a DataFrame in Pandas?" the system retrieves accurate chunks. At time 14:50, you can compare the results with the actual video transcript.

![Original Content](./original_content.png)
![Chunk Output](./chunk_output.png)

## Conclusion

The strategy of chunking by character length with overlap strikes a balance between readability and efficient retrieval. Using `RecursiveCharacterTextSplitter`, we ensure chunks are clear and complete, with important information not being cut off. The overlap helps maintain key details across chunks, making the system capable of providing accurate and useful responses. This method is effective for processing and managing video transcript data in the challenge.
