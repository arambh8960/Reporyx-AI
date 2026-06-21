<div align="center">

# 🚀 Reporyx-AI

### AI-Powered Developer Onboarding Assistant for GitHub Repositories

![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-10b981?style=for-the-badge&logo=mongodb)
![ChromaDB](https://img.shields.io/badge/Vector%20Database-ChromaDB-f59e0b?style=for-the-badge)
![Groq](https://img.shields.io/badge/AI-Groq%20%2B%20Llama-6366f1?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

**Reporyx-AI** is an AI-powered developer onboarding platform that helps developers understand any GitHub repository faster using **Retrieval-Augmented Generation (RAG)**, **semantic code search**, and **repository-aware AI conversations**.

Instead of manually exploring hundreds of files, developers can simply paste a GitHub repository URL and start asking questions about the codebase in natural language.

**Built for developers, students, open-source contributors, and engineering teams.**

</div>

---

# ✨ Why Reporyx-AI?

Understanding a new codebase is one of the biggest challenges for developers.

Whether you're:

- Joining a new company
- Contributing to open source
- Working on a team project
- Exploring an unfamiliar GitHub repository

You often spend hours reading documentation, searching files, and tracing code manually.

Reporyx-AI reduces that effort by converting an entire repository into an AI-searchable knowledge base.

Simply provide a GitHub repository URL and ask:

> "How does authentication work?"

> "What technologies are used?"

> "Explain this repository to a new developer."

> "Where is the API logic implemented?"

And receive answers grounded in the actual source code.

---

# 🚀 Features

## 📂 Repository Analysis

- Clone and analyze any public GitHub repository
- Detect technologies and frameworks automatically
- Generate repository structure overview
- Extract README information
- Generate AI-powered repository summaries
- Analyze files and folders

---

## 🧠 AI Repository Assistant

- Ask questions about any repository
- Natural language codebase interaction
- Repository-aware conversations
- Context-aware responses
- Source-grounded answers

---

## 🔍 Semantic Code Search

- Intelligent code retrieval
- Multi-file context understanding
- Similarity-based search
- Relevant code chunk retrieval
- Better than traditional keyword search

---

## ⚡ RAG Pipeline

- Source code chunking
- Embedding generation
- ChromaDB vector storage
- Semantic retrieval
- Context aggregation
- LLM-powered response generation

---

## 🎯 Developer Onboarding

- Understand repositories faster
- Identify important project components
- Learn architecture quickly
- Reduce onboarding time
- Improve developer productivity

---

# 🛠️ Tech Stack

| Layer | Technology |
|---------|-------------|
| Frontend | React.js, Vite, Tailwind CSS, Axios |
| Backend | FastAPI, Python |
| Database | MongoDB Atlas |
| Vector Database | ChromaDB |
| AI Model | Groq API (Llama 3.3 70B) |
| Embeddings | Sentence Transformers |
| Repository Processing | GitPython |

---

# 🏗️ System Architecture

```text
User
 │
 ▼
React Frontend
 │
 ▼
FastAPI Backend
 │
 ├── Repository Analyzer
 ├── Code Reader
 ├── Chunking Service
 ├── Embedding Service
 ├── ChromaDB Vector Store
 ├── Retrieval Engine
 └── Groq LLM
          │
          ▼
     AI Response
```

---

# 📂 Project Structure

```text
Reporyx-AI
│
├── backend
│   ├── database
│   ├── models
│   ├── routes
│   ├── services
│   ├── repositories
│   ├── chroma_db
│   └── main.py
│
├── frontend
│   ├── public
│   ├── src
│   │   ├── components
│   │   ├── pages
│   │   ├── services
│   │   └── assets
│   └── package.json
│
└── README.md
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/arambh8960/CodeGraph-AI.git

cd CodeGraph-AI
```

---

# 🔧 Backend Setup

```bash
cd backend

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
MONGODB_URL=your_mongodb_url

GROQ_API_KEY=your_groq_api_key

JWT_SECRET_KEY=your_secret_key

JWT_ALGORITHM=HS256

JWT_EXPIRE_MINUTES=60
```

---

# 🚀 Run Backend

```bash
cd backend

source venv/bin/activate

./venv/bin/python -m uvicorn main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

# 🎨 Frontend Setup

```bash
cd frontend

npm install
```

Create a `.env` file:

```env
VITE_API_URL=http://127.0.0.1:8000
```

---

# 🚀 Run Frontend

```bash
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

# 🔄 How It Works

### 1️⃣ Repository Submission

User provides a GitHub repository URL.

### 2️⃣ Repository Processing

Reporyx-AI clones the repository and extracts source files.

### 3️⃣ Code Chunking

Large source files are split into meaningful chunks.

### 4️⃣ Embedding Generation

Embeddings are generated using Sentence Transformers.

### 5️⃣ Vector Storage

Embeddings are stored inside ChromaDB.

### 6️⃣ Semantic Retrieval

Relevant code chunks are retrieved based on user queries.

### 7️⃣ AI Response Generation

Groq Llama generates repository-aware responses using retrieved context.

---

# 🎯 Example Questions

```text
What is the architecture of this repository?

Which technologies are used?

Explain this project to a beginner.

How does the backend work?

Where is authentication implemented?

What are the main files in this project?

Summarize this repository.

How does the frontend communicate with the backend?
```

---

# 🌟 Key Highlights

✅ Repository-Aware AI Assistant

✅ Semantic Code Search

✅ Retrieval-Augmented Generation (RAG)

✅ Multi-File Context Retrieval

✅ ChromaDB Vector Search

✅ Technology Detection

✅ Repository Summary Generation

✅ Developer Onboarding Support

✅ Source-Grounded AI Responses

---

# 🚀 Future Scope

- GraphRAG Integration
- Repository Visualization
- Multi-Repository Analysis
- Automated Documentation Generation
- Pull Request Understanding
- Code Change Impact Analysis
- Team Knowledge Assistant

---

# 🎯 Project Goal

Reporyx-AI aims to reduce the time required to understand unfamiliar codebases by combining repository analysis, semantic retrieval, and AI-powered code understanding into a single platform.

---

# 👨‍💻 Developer

### Arambh Tiwari

B.Tech CSE | MERN Stack Developer | AI Enthusiast

GitHub: https://github.com/arambh8960

---

<div align="center">

⭐ If you found this project useful, please consider giving it a star! ⭐

</div>
