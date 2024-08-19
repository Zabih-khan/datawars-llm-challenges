# Evaluation Metrics for RAG Chunking

## Objective
The goal is to evaluate the effectiveness of the chunking strategy used for processing video transcripts to ensure high relevance, correctness, and cost efficiency.

## Metrics

### 1. Relevancy
- **Definition:** The degree to which each chunk retains meaningful and contextually coherent information.
- **Evaluation:** Check if chunks include full ideas or concepts rather than splitting them inappropriately. This can be tested by querying the vector store and assessing the relevance of retrieved chunks.

### 2. Correctness
- **Definition:** The ability of each chunk to accurately represent the content of the transcript without omitting critical information.
- **Evaluation:** Compare the chunks against the original transcript to ensure important details are not lost or fragmented.

### 3. Cost Efficiency
- **Definition:** The computational and financial cost of processing and querying chunks.
- **Evaluation:** Analyze the token usage for various chunk sizes and overlaps. A balance between chunk size and overlap should minimize token costs while retaining information.

## Challenges Faced
- Balancing between large chunk sizes for cost efficiency and smaller chunks for better accuracy and relevance.
- Ensuring that overlapping text does not introduce redundancy or confusion.

## Conclusion
The chosen strategy of chunking by character length with overlap should provide a good balance, but further testing and adjustments may be necessary based on the evaluation results.
