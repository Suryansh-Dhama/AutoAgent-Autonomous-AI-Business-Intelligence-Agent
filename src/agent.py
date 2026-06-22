from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from typing import TypedDict, List
import os

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

# Agent State
class AgentState(TypedDict):
    messages: List[str]
    current_step: str
    final_answer: str

# Node 1 - Think
def think_node(state: AgentState):
    user_input = state["messages"][-1]
    response = llm.invoke(f"Analyze this query and decide what to do: {user_input}")
    return {
        "messages": state["messages"] + [response.content],
        "current_step": "think"
    }

# Node 2 - Answer
def answer_node(state: AgentState):
    context = "\n".join(state["messages"])
    response = llm.invoke(f"Give final answer based on: {context}")
    return {
        "final_answer": response.content,
        "current_step": "done"
    }

# Graph banana
def create_agent():
    graph = StateGraph(AgentState)
    
    graph.add_node("think", think_node)
    graph.add_node("answer", answer_node)
    
    graph.set_entry_point("think")
    graph.add_edge("think", "answer")
    graph.add_edge("answer", END)
    
    return graph.compile()

if __name__ == "__main__":
    agent = create_agent()
    
    result = agent.invoke({
        "messages": ["What is LangGraph and why is it useful?"],
        "current_step": "",
        "final_answer": ""
    })
    
    print("=== AGENT RESPONSE ===")
    print(result["final_answer"])