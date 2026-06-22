from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

response = llm.invoke("Hello! Ek line mein bata tu kya kar sakta hai?")
print(response.content)