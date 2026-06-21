<div align="center">

# 🚀 Reporyx-AI

### AI-Powered Developer Onboarding Assistant for GitHub Repositories

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge)]()
[![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=for-the-badge)]()
[![MongoDB](https://img.shields.io/badge/Database-MongoDB-10b981?style=for-the-badge)]()
[![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-f59e0b?style=for-the-badge)]()
[![Groq AI](https://img.shields.io/badge/AI-Groq%20%2B%20Llama-6366f1?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

**Reporyx-AI** is an AI-powered developer onboarding platform that helps developers understand any GitHub repository instantly using Retrieval-Augmented Generation (RAG), semantic code search, architecture analysis, dependency tracing, and intelligent repository Q&A.

Instead of manually reading hundreds of files, developers can simply provide a GitHub repository URL and ask questions in natural language.

[⚙️ Features](#-features)  ·  [🛠️ Installation](#️-installation)  ·  [🏗️ Architecture](#️-system-architecture)  ·  [📂 Project Structure](#-project-structure)

</div>

---

# ✨ What Makes Reporyx-AI Different?

Most AI code assistants answer questions from a few retrieved files.

Reporyx-AI goes beyond simple repository chat by understanding the repository structure, tracing execution flow, identifying entry points, analyzing dependencies, and generating onboarding guidance for developers.

Ask questions like:

* "What is the architecture of this repository?"
* "Where does authentication start?"
* "Explain the login flow step by step."
* "Which files are responsible for API routing?"
* "What is the entry point of this project?"
* "Generate an onboarding plan for new developers."

And receive repository-aware answers backed by actual source code.

---

# 🚀 Features

## 📂 Repository Analysis

* Analyze any public GitHub repository
* Automatic repository cloning
* Technology stack detection
* Repository structure analysis
* README extraction
* AI-generated repository summary
* File and folder statistics

## 🧠 AI-Powered Repository Understanding

* Natural language repository Q&A
* Semantic code search
* Multi-file retrieval
* Source-aware responses
* Intelligent code explanations
* Context-aware code understanding

## 🔍 RAG Pipeline

* Automatic code chunking
* Embedding generation
* ChromaDB vector storage
* Semantic similarity search
* Repository-specific retrieval
* Context aggregation

## 🏗️ Architecture Analysis

* Project structure understanding
* Folder hierarchy analysis
* Architecture overview generation
* Layer detection
* Repository navigation support

## 🔗 Dependency & Flow Analysis

* Dependency graph generation
* Import relationship mapping
* Entry point detection
* Request flow tracing
* Function call tracing
* Component interaction understanding

## 🎯 Developer Onboarding

* Smart onboarding guidance
* Repository walkthrough
* Key file identification
* Learning path generation
* Faster developer ramp-up

---

# 🛠️ Tech Stack

| Layer                 | Technology                          |
| --------------------- | ----------------------------------- |
| Frontend              | React.js, Vite, Tailwind CSS, Axios |
| Backend               | FastAPI, Python                     |
| Database              | MongoDB Atlas                       |
| Vector Database       | ChromaDB                            |
| LLM                   | Groq API (Llama 3.3 70B)            |
| Embeddings            | Sentence Transformers               |
| Repository Processing | GitPython                           |
| Graph Analysis        | NetworkX                            |

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
 ├── Architecture Analyzer
 ├── Dependency Graph Builder
 └── Flow Tracing Engine
          │
          ▼
      Groq LLM
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
│   ├── utils
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

```bash
git clone https://github.com/arambh8960/Reporyx-AI.git

cd Reporyx-AI
```

---

## Backend Setup

```bash
cd backend

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file inside the backend folder:

```env
MONGODB_URL=your_mongodb_url

GROQ_API_KEY=your_groq_api_key

JWT_SECRET_KEY=your_secret_key

JWT_ALGORITHM=HS256

JWT_EXPIRE_MINUTES=60
```

### Run Backend

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

## Frontend Setup

```bash
cd frontend

npm install
```

Create a `.env` file:

```env
VITE_API_URL=http://127.0.0.1:8000
```

### Run Frontend

```bash
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

# 🔄 How It Works

### Step 1

User enters a GitHub repository URL.

### Step 2

Reporyx-AI clones the repository locally.

### Step 3

Repository files are extracted and analyzed.

### Step 4

Source code is chunked into semantic sections.

### Step 5

Embeddings are generated using Sentence Transformers.

### Step 6

Embeddings are stored in ChromaDB.

### Step 7

User asks repository-related questions.

### Step 8

Relevant code chunks are retrieved using semantic search.

### Step 9

Groq LLM generates repository-aware answers.

---

# 🎯 Example Questions

```text
What is the architecture of this repository?

Explain the authentication flow.

What is the entry point of this project?

Trace the login workflow.

Which files are responsible for API routing?

How does the frontend communicate with the backend?

Generate an onboarding plan for a new developer.

Explain the dependency graph.

What technologies are used in this repository?
```

---

# 🌟 Unique Features

✅ Repository-Aware AI Assistant

✅ Semantic Code Retrieval

✅ Architecture Understanding

✅ Dependency Graph Generation

✅ Flow Tracing Engine

✅ Entry Point Detection

✅ Developer Onboarding Guidance

✅ Multi-File Context Retrieval

✅ Source-Aware Responses

---

# 🚀 Future Improvements

* GraphRAG Integration
* Neo4j Knowledge Graph
* Interactive Dependency Visualization
* Multi-Repository Analysis
* Pull Request Understanding
* Code Change Impact Analysis
* Automated Documentation Generation
* Team Onboarding Assistant

---

# 👨‍💻 Developer

**Arambh Tiwari**

B.Tech CSE | MERN Stack Developer | AI Enthusiast

GitHub: https://github.com/arambh8960

---

<div align="center">

⭐ If you found this project useful, consider giving it a star! ⭐

</div>
