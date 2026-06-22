from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.main_agent import create_main_agent
from memory.memory import get_history_as_string, add_to_memory

app = FastAPI(
    title="AutoAgent API",
    description="Autonomous AI Business Intelligence Agent",
    version="1.0.0"
)

agent = create_main_agent()

# Request Model
class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = "default"

# Response Model
class QueryResponse(BaseModel):
    query: str
    answer: str
    tool_used: str
    status: str

@app.get("/")
def root():
    return {
        "message": "AutoAgent API is running!",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
def query_agent(request: QueryRequest):
    try:
        history = get_history_as_string(request.user_id)
        
        result = agent.invoke({
            "query": request.query,
            "user_id": request.user_id,
            "chat_history": history,
            "search_results": "",
            "rag_results": "",
            "final_answer": "",
            "tool_used": ""
        })
        
        return QueryResponse(
            query=request.query,
            answer=result["final_answer"],
            tool_used=result["tool_used"],
            status="success"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.post("/add-documents")
def add_docs(texts: list[str]):
    try:
        from tools.rag_tool import add_documents
        result = add_documents(texts)
        return {"message": result, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))