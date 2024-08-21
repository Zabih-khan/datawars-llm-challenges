import json
import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_chroma import Chroma
from langchain.docstore.document import Document
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_openai import OpenAIEmbeddings

print("Loading environment variables from .env file...")
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

print("Initializing LLM and embedding model...")
llm = OpenAI(api_key=api_key)
embedding = OpenAIEmbeddings(api_key=api_key)

current_directory = os.getcwd()
chunks_file = os.path.join(current_directory, "chunks_output", "chunks.json")
print(f"Loading chunks of text from JSON file: {chunks_file}...")
with open(chunks_file, "r") as file:
    chunks = json.load(file)

print("Preparing documents for vector store...")
documents = [Document(page_content=chunk["text"], metadata=chunk) for chunk in chunks]

print("Creating Chroma vector store from documents...")
vectorstore = Chroma.from_documents(documents, embedding=embedding, persist_directory="./vectorstore")

print("Setting up retriever for document search...")
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

print("Creating the prompt template for the LLM...")
prompt_template = ChatPromptTemplate.from_template(
    """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

Question: {input} 

Context: {context} 

Answer:

    """
)

print("Creating Retrieval-Augmented Generation (RAG) chain...")
document_chain = create_stuff_documents_chain(llm, prompt_template)
rag_chain = create_retrieval_chain(retriever, document_chain)

query = "How can I group a DataFrame in Pandas?"
print(f"Executing query: '{query}'...")
response = rag_chain.invoke({"input": query})

print("Response from the assistant:")
print(response['answer'])
