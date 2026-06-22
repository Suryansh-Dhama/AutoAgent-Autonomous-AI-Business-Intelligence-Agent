from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# Text splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

def add_documents(texts: list, collection_name: str = "autoagent"):
    """Documents ko vector store mein add karta hai"""
    chunks = splitter.create_documents(texts)
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory="./data/chroma"
    )
    
    return f"{len(chunks)} chunks added successfully!"

def search_documents(query: str, collection_name: str = "autoagent") -> str:
    """Vector store se relevant documents dhundta hai"""
    try:
        vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory="./data/chroma"
        )
        
        results = vectorstore.similarity_search(query, k=3)
        
        if not results:
            return "No relevant documents found."
        
        output = []
        for i, doc in enumerate(results):
            output.append(f"Result {i+1}:\n{doc.page_content}\n")
        
        return "\n".join(output)
    
    except Exception as e:
        return f"RAG error: {str(e)}"

if __name__ == "__main__":
    # Test documents add karo
    sample_texts = [
        "AutoAgent is an AI powered business intelligence system built with LangGraph and LangChain.",
        "The system uses Groq LLM with Llama 3.3 70B model for fast inference.",
        "RAG pipeline uses ChromaDB for vector storage and HuggingFace embeddings.",
        "FastAPI backend provides REST API endpoints for the agent.",
        "Redis is used for short term memory management in the agent."
    ]
    
    print(add_documents(sample_texts))
    
    print("\n=== RAG SEARCH ===")
    result = search_documents("What LLM does AutoAgent use?")
    print(result)