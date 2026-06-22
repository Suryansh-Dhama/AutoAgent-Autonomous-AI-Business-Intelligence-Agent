from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from typing import TypedDict, List
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.search_tool import web_search
from tools.rag_tool import search_documents
from memory.memory import add_to_memory, get_history_as_string

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

# Agent State
class AgentState(TypedDict):
    query: str
    user_id: str
    chat_history: str
    search_results: str
    rag_results: str
    final_answer: str
    tool_used: str

# Node 1 - Query Analyze
def analyze_node(state: AgentState):
    query = state["query"]
    history = state["chat_history"]
    
    response = llm.invoke(f"""
    You are an AI assistant. Analyze this query and respond with ONLY one word:
    - 'search' if it needs current/real-time information
    - 'rag' if it can be answered from stored documents
    
    Previous conversation:
    {history}
    
    Current Query: {query}
    """)
    
    tool = response.content.strip().lower()
    if "search" in tool:
        tool = "search"
    else:
        tool = "rag"
    
    return {"tool_used": tool}

# Node 2 - Web Search
def search_node(state: AgentState):
    results = web_search(state["query"])
    return {"search_results": results}

# Node 3 - RAG Search
def rag_node(state: AgentState):
    results = search_documents(state["query"])
    return {"rag_results": results}

# Node 4 - Final Answer
def answer_node(state: AgentState):
    query = state["query"]
    user_id = state["user_id"]
    history = state["chat_history"]
    context = state.get("search_results", "") or state.get("rag_results", "")
    tool = state["tool_used"]
    
    response = llm.invoke(f"""
    You are AutoAgent, an AI Business Intelligence Assistant.
    
    Previous Conversation:
    {history}
    
    Current Query: {query}
    Context: {context}
    Tool Used: {tool}
    
    Give a clear, detailed answer. Remember previous conversation context.
    """)
    
    # Memory mein save karo
    add_to_memory(user_id, query, response.content)
    
    return {"final_answer": response.content}

# Router
def route_tool(state: AgentState):
    if state["tool_used"] == "search":
        return "search"
    return "rag"

# Graph banana
def create_main_agent():
    graph = StateGraph(AgentState)
    
    graph.add_node("analyze", analyze_node)
    graph.add_node("search", search_node)
    graph.add_node("rag", rag_node)
    graph.add_node("answer", answer_node)
    
    graph.set_entry_point("analyze")
    
    graph.add_conditional_edges(
        "analyze",
        route_tool,
        {
            "search": "search",
            "rag": "rag"
        }
    )
    
    graph.add_edge("search", "answer")
    graph.add_edge("rag", "answer")
    graph.add_edge("answer", END)
    
    return graph.compile()

if __name__ == "__main__":
    agent = create_main_agent()
    
    print("=== TEST WITH MEMORY ===")
    
    result1 = agent.invoke({
        "query": "What is LangGraph?",
        "user_id": "test_user",
        "chat_history": "",
        "search_results": "",
        "rag_results": "",
        "final_answer": "",
        "tool_used": ""
    })
    print(f"Q1: {result1['final_answer'][:200]}...")
    
    result2 = agent.invoke({
        "query": "Tell me more about it",
        "user_id": "test_user",
        "chat_history": get_history_as_string("test_user"),
        "search_results": "",
        "rag_results": "",
        "final_answer": "",
        "tool_used": ""
    })
    print(f"\nQ2: {result2['final_answer'][:200]}...")