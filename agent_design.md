

# Define the Prompts

```
The agent provides the student with a concise answer and includes the video title and timestamp for further reference.


You are an assistant for answering questions based on educational content about Pandas and Matplotlib. Use the following pieces of context to answer the question. If you don't know the answer, state that you don't know. Keep your answer concise and relevant to the question.

Question: {input}

Context: {context}

Answer:

```

# Implement the Retrieval-Augmented Generation (RAG) Chain
**Retrieve Context:** Use the vector store to fetch relevant chunks based on the user's query.
**Generate Response:** Use the LLM to generate an answer based on the retrieved context and the defined prompts.



# Agent Workflow

## 1. User Input
The student inputs a question, such as "How do I group a DataFrame in Pandas?"

## 2. Query the Vector Store
The agent retrieves the most relevant transcript chunks using similarity search based on embeddings.

## 3. Generate a Response
The agent combines the retrieved transcript chunks and user query into the final prompt for the language model to generate an answer.