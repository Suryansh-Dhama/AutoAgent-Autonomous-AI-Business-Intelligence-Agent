from pypdf import PdfReader
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.rag_tool import add_documents

def extract_text_from_pdf(pdf_path: str) -> str:
    """PDF se text extract karo"""
    try:
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def process_pdf(pdf_path: str, collection_name: str = "autoagent") -> str:
    """PDF ko process karke RAG mein add karo"""
    try:
        print(f"Extracting text from {pdf_path}...")
        text = extract_text_from_pdf(pdf_path)
        
        if not text:
            return "No text found in PDF!"
        
        print("Adding to RAG pipeline...")
        result = add_documents([text], collection_name)
        
        return f"PDF processed successfully! {result}"
    
    except Exception as e:
        return f"Error processing PDF: {str(e)}"

if __name__ == "__main__":
    test_text = """
    AutoAgent Documentation
    AutoAgent is an Autonomous AI Business Intelligence Agent.
    It uses LangGraph for orchestration and Groq LLM for inference.
    The system supports web search via Tavily and document search via ChromaDB.
    FastAPI provides REST API endpoints and Streamlit provides the chat UI.
    """
    
    print("=== PDF TOOL TEST ===")
    result = add_documents([test_text], "autoagent")
    print(result)
    print("PDF Tool Working!")