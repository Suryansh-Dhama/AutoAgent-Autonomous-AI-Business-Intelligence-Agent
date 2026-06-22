from langchain_core.messages import HumanMessage, AIMessage
from typing import Dict, List

# In-memory store
chat_histories: Dict[str, List] = {}

def add_to_memory(user_id: str, human_msg: str, ai_msg: str):
    """Conversation memory mein add karo"""
    if user_id not in chat_histories:
        chat_histories[user_id] = []
    
    chat_histories[user_id].append(HumanMessage(content=human_msg))
    chat_histories[user_id].append(AIMessage(content=ai_msg))

def get_chat_history(user_id: str) -> list:
    """User ki puri chat history lo"""
    if user_id not in chat_histories:
        return []
    
    messages = []
    for msg in chat_histories[user_id]:
        if isinstance(msg, HumanMessage):
            messages.append({"role": "user", "content": msg.content})
        else:
            messages.append({"role": "assistant", "content": msg.content})
    
    return messages

def clear_memory(user_id: str):
    """User ki memory clear karo"""
    if user_id in chat_histories:
        chat_histories[user_id] = []
    return "Memory cleared!"

def get_history_as_string(user_id: str) -> str:
    """History string format mein lo"""
    history = get_chat_history(user_id)
    if not history:
        return "No previous conversation."
    
    result = []
    for msg in history:
        result.append(f"{msg['role'].upper()}: {msg['content']}")
    
    return "\n".join(result)

if __name__ == "__main__":
    add_to_memory("user1", "What is AI?", "AI is Artificial Intelligence.")
    add_to_memory("user1", "Tell me more", "AI includes ML, DL, NLP...")
    
    print("=== CHAT HISTORY ===")
    history = get_chat_history("user1")
    for msg in history:
        print(f"{msg['role']}: {msg['content']}")
    
    print("\n=== HISTORY AS STRING ===")
    print(get_history_as_string("user1"))