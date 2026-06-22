import streamlit as st
import requests
import json
import os
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.tools.pdf_tool import process_pdf
from src.memory.memory import get_chat_history, clear_memory

# Page Config
st.set_page_config(
    page_title="AutoAgent — AI Business Intelligence",
    page_icon="🤖",
    layout="wide"
)

# Header
st.title("🤖 AutoAgent")
st.subheader("Autonomous AI Business Intelligence Agent")
st.divider()

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.info("""
    **AutoAgent** is an AI powered Business Intelligence system.
    
    It can:
    - 🔍 Search the web in real-time
    - 📚 Search stored documents
    - 🧠 Auto-decide which tool to use
    - 📄 Process PDF documents
    - 💾 Remember conversations
    """)
    
    st.header("⚙️ Settings")
    api_url = st.text_input(
        "API URL",
        value="http://127.0.0.1:8000"
    )
    
    user_id = st.text_input(
        "User ID",
        value="default_user"
    )
    
    st.header("📄 Upload PDF")
    uploaded_file = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"]
    )
    
    if uploaded_file is not None:
        if st.button("Process PDF"):
            with st.spinner("Processing PDF..."):
                try:
                    # Temp file mein save karo
                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf"
                    ) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    result = process_pdf(tmp_path)
                    os.unlink(tmp_path)
                    st.success(result)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    st.header("📊 Stats")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("API Health"):
            try:
                response = requests.get(f"{api_url}/health")
                if response.status_code == 200:
                    st.success("Healthy! ✅")
                else:
                    st.error("Down! ❌")
            except:
                st.error("Error! ❌")
    
    with col2:
        if st.button("Clear Memory"):
            clear_memory(user_id)
            st.session_state.messages = []
            st.success("Cleared! ✅")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_id" not in st.session_state:
    st.session_state.user_id = "default_user"

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "tool_used" in message:
            st.caption(f"🔧 Tool Used: **{message['tool_used']}**")

# Chat Input
if prompt := st.chat_input("Ask me anything..."):
    
    # User Message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Agent Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{api_url}/query",
                    json={
                        "query": prompt,
                        "user_id": user_id
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    tool_used = data["tool_used"]
                    
                    st.markdown(answer)
                    st.caption(f"🔧 Tool Used: **{tool_used}**")
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "tool_used": tool_used
                    })
                else:
                    st.error("API Error!")
                    
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")