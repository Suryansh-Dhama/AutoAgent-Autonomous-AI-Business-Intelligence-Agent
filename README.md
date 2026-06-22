<div align="center">

# 🤖 AutoAgent
### Autonomous AI Business Intelligence Agent

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-green?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-orange?style=for-the-badge)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Suryansh-Dhama/AutoAgent?style=for-the-badge)](https://github.com/Suryansh-Dhama/AutoAgent/stargazers)
[![Forks](https://img.shields.io/github/forks/Suryansh-Dhama/AutoAgent?style=for-the-badge)](https://github.com/Suryansh-Dhama/AutoAgent/network/members)

> **AutoAgent** is a production-ready autonomous AI agent that intelligently searches the web in real-time, processes private documents via RAG, remembers multi-turn conversations, and delivers structured business intelligence — all powered by LangGraph orchestration and Groq's blazing-fast Llama 3.3 70B.

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🏗️ Architecture](#-architecture) • [🤝 Contributing](#-contributing) • [📄 License](#-license)

</div>

---

## ✨ Features

- 🔍 **Real-time Web Search** — Tavily API se live internet data fetch karta hai
- 📚 **RAG Pipeline** — ChromaDB vector store se private documents search karta hai
- 🧠 **Smart Tool Routing** — Agent khud decide karta hai web search ya RAG use karna hai
- 💾 **Conversation Memory** — Multi-turn conversations yaad rakhta hai
- 📄 **PDF Processing** — PDF upload karo, agent khud process karega
- ⚡ **Blazing Fast** — Groq + Llama 3.3 70B se ultra-fast inference
- 🌐 **REST API** — Production-ready FastAPI backend
- 💬 **Chat UI** — Beautiful Streamlit frontend
- 🐳 **Docker Ready** — One command deployment

---

## 🏗️ Architecture

```
User Query
     │
     ▼
┌─────────────┐
│ Streamlit   │  ◄── Beautiful Chat UI
│    UI       │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  FastAPI    │  ◄── REST API Backend
│  Backend    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  LangGraph  │  ◄── Agent Orchestration
│   Agent     │
└──────┬──────┘
       │
       ▼
┌──────────────────────┐
│     Analyze Node     │  ◄── Query Analysis
└──────┬───────────────┘
       │
  ┌────┴────┐
  ▼         ▼
Search     RAG
 Node      Node
(Tavily) (ChromaDB)
  │         │
  └────┬────┘
       ▼
┌─────────────┐
│ Answer Node │  ◄── Groq Llama 3.3 70B
└─────────────┘
       │
       ▼
  Final Answer
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **LLM** | Groq + Llama 3.3 70B | Fast inference |
| **Orchestration** | LangGraph | Agent workflow |
| **Framework** | LangChain | LLM framework |
| **Vector Store** | ChromaDB | Document storage |
| **Embeddings** | HuggingFace | Text embeddings |
| **Web Search** | Tavily API | Real-time search |
| **Backend** | FastAPI | REST API |
| **Frontend** | Streamlit | Chat UI |
| **Deployment** | Docker | Containerization |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Groq API Key — [Get here](https://console.groq.com)
- Tavily API Key — [Get here](https://tavily.com)

### Installation

**1. Clone the repo**
```bash
git clone https://github.com/Suryansh-Dhama/AutoAgent.git
cd AutoAgent
```

**2. Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Setup environment variables**
```bash
cp .env.example .env
# Add your API keys in .env file
```

**5. Run FastAPI backend**
```bash
uvicorn src.api.main:app --reload
```

**6. Run Streamlit frontend** (new terminal)
```bash
python -m streamlit run app.py
```

**7. Open browser**
```
http://localhost:8501
```

---

## 🐳 Docker Setup

```bash
docker-compose up --build
```

---

## 📁 Project Structure

```
AutoAgent/
├── src/
│   ├── agents/
│   │   └── main_agent.py      # LangGraph agent
│   ├── tools/
│   │   ├── search_tool.py     # Tavily web search
│   │   ├── rag_tool.py        # ChromaDB RAG
│   │   └── pdf_tool.py        # PDF processing
│   ├── memory/
│   │   └── memory.py          # Conversation memory
│   └── api/
│       └── main.py            # FastAPI endpoints
├── data/                      # Vector store data
├── app.py                     # Streamlit UI
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🔑 Environment Variables

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API status |
| GET | `/health` | Health check |
| POST | `/query` | Query the agent |
| POST | `/add-documents` | Add documents to RAG |

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** your feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Good First Issues
- [ ] Add streaming responses
- [ ] Add authentication system
- [ ] Add more LLM providers
- [ ] Add data visualization
- [ ] Add voice input support
- [ ] Improve error handling
- [ ] Add unit tests

---

## 📊 Roadmap

- [x] LangGraph Agent
- [x] Web Search Tool
- [x] RAG Pipeline
- [x] Conversation Memory
- [x] PDF Processing
- [x] FastAPI Backend
- [x] Streamlit UI
- [x] Docker Support
- [ ] Streaming Responses
- [ ] Authentication
- [ ] Voice Input
- [ ] Data Visualization
- [ ] Cloud Deployment

---

## 👨‍💻 Author

**Suryansh Dhama**

[![GitHub](https://img.shields.io/badge/GitHub-Suryansh--Dhama-black?style=flat&logo=github)](https://github.com/Suryansh-Dhama)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-suryansh--dhama-blue?style=flat&logo=linkedin)](https://linkedin.com/in/suryansh-dhama-7217a428b)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## ⭐ Support

Agar yeh project helpful laga toh **Star** zaroor dena! 🌟

</div>
