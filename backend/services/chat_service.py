import os
from groq import Groq, RateLimitError
from dotenv import load_dotenv

from services.retrieval_service import retrieve_relevant_files
from services.architecture_service import analyze_architecture
from services.flow_tracing_service import extract_code_entities
from services.flow_graph_service import (
    build_flow_graph,
    format_graph
)

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

ARCHITECTURE_KEYWORDS = [
    "architecture", "backend architecture", "frontend architecture",
    "project structure", "folder structure", "repository structure",
    "system design", "design", "layout"
]

FLOW_KEYWORDS = ["flow", "workflow", "how does", "working", "explain"]

async def ask_repository(question: str, repo_name: str, history: list):
    is_architecture_question = any(keyword in question.lower() for keyword in ARCHITECTURE_KEYWORDS)
    repo_path = os.path.join("..", "data", "repositories", repo_name)
    
    q_lower = question.lower()
    
    # 1. Architecture handled without LLM
    if is_architecture_question:
        architecture = analyze_architecture(repo_path)
        get_dirs = lambda key: ", ".join(d["directory"] for d in architecture.get(key, []))
        get_list = lambda key: ", ".join(architecture.get(key, []))
        
        answer = f"""
Repository Status: {architecture.get("repository_status")}
System Entry Points: {get_list("system_entry_points") or "None"}
Configurations: {get_list("build_and_configurations") or "None"}
Communication Layers: {get_dirs("communication_layers") or "None"}
Core Layers: {get_dirs("core_implementation_layers") or "None"}
"""
        return {
            "answer": answer.strip(),
            "sources": architecture.get("system_entry_points", [])[:3]
        }

    # 2. Query Rewriting removed (Generic)
    retrieval_query = question

    files = await retrieve_relevant_files(repo_name, retrieval_query)
    
    if not files:
        return {"answer": "No relevant repository files found.", "sources": []}
        
    ordered_files = files[:8]

    graph_context = ""
    if any(k in q_lower for k in FLOW_KEYWORDS):
        entities = extract_code_entities(ordered_files)
        graph = build_flow_graph(entities)
        graph_context = format_graph(graph)

    # 3. Context Construction (Updated parameters)
    context = ""
    MAX_CONTEXT = 12000
    MAX_PER_FILE = 2500
    used = 0
    
    for file in ordered_files:
        remaining = MAX_CONTEXT - used
        if remaining <= 0: break
        content = file.get("content", "")
        chunk = content[:min(MAX_PER_FILE, remaining)]
        block = f"\n--- START FILE: {file['file_path']} ---\n{chunk}\n--- END FILE: {file['file_path']} ---\n"
        context += block
        used += len(block)
    
    sources = [f["file_path"] for f in ordered_files[:3]]

    # Prompt with updated Rules
    prompt = f"""
Question:
{question}

Relevant Repository Context:
{context}

Flow Graph:
{graph_context}


Rules:
1. Use ONLY provided repository context.
2. Mention exact source files.
3. If implementation exists in context, COPY the implementation exactly.
4. Never summarize implementation code.
5. Never replace code with explanation.
6. If code exists in context, return the code block first, then explanation if needed.
7. For flow questions, trace execution step-by-step using the provided files.
8. Do not invent functions, files, or logic.
9. If information is missing, say: "Not found in repository context."
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        return {
            "answer": response.choices[0].message.content,
            "sources": sources
        }
    except RateLimitError:
        return {"answer": "Groq daily token limit reached.", "sources": []}
    except Exception as e:
        return {"answer": f"Error generating answer: {str(e)}", "sources": []}