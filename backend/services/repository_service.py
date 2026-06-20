import os
import shutil
from git import Repo

from services.repository_summary_service import generate_repository_summary
from services.ai_summary_service import generate_ai_summary
from services.code_reader_service import extract_code_files
from services.vector_storage_service import (
    save_embeddings,
    delete_repo_vectors
)

def extract_repo_name(repo_url: str):
    """Strips query parameters and securely extracts target repository root token."""
    clean_url = repo_url.split("?")[0]
    return clean_url.rstrip("/").split("/")[-1]


def process_repository_topology(repo_path):
    """
    Hybrid Language-Agnostic Single-Walk Repository Parser.
    Uses case-insensitive file markers and extension lookups to build a 
    deterministic, alphabetically sorted technology signature matrix.
    """
    file_count = 0
    folder_count = 0
    technologies = set()
    tree = []

    # Pure language extensions only (Accurate UI Component extensions included)
    EXTENSION_TECH_MAP = {
        ".py": "Python", 
        ".js": "JavaScript", 
        ".ts": "TypeScript", 
        ".jsx": "JSX", 
        ".tsx": "TSX", 
        ".go": "Go", 
        ".rs": "Rust", 
        ".java": "Java", 
        ".cpp": "C++", 
        ".c": "C", 
        ".cs": "C#", 
        ".rb": "Ruby", 
        ".php": "PHP", 
        ".swift": "Swift",
        ".kt": "Kotlin", 
        ".sh": "ShellScript", 
        ".ex": "Elixir", 
        ".zig": "Zig"
    }

    # Core Ecosystem Metadata Markers (Normalized keys to strict lowercase)
    FILE_MARKER_TECH_MAP = {
        "package.json": "Node.js",
        "requirements.txt": "Python",
        "go.mod": "Go",
        "cargo.toml": "Rust",
        "pom.xml": "Java",
        "build.gradle": "Java/Kotlin",
        "cmakelists.txt": "C++",
        "gemfile": "Ruby",
        "mix.exs": "Elixir"
    }

    IGNORE_DIRS = {
        ".git", "node_modules", "__pycache__", "dist", "build", 
        ".next", ".nuxt", "coverage", "target", "bin", "obj", 
        "vendor", ".idea", ".vscode", "venv", ".env"
    }

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        folder_count += len(dirs)
        relative_path = os.path.relpath(root, repo_path)

        if relative_path != ".":
            tree.append(relative_path + "/")

        for file in files:
            if file.startswith("."):
                continue

            file_count += 1
            file_path = file if relative_path == "." else os.path.join(relative_path, file)
            tree.append(file_path)

            # 1. Case-Insensitive Ecosystem Metadata Marker Match
            file_lower = file.lower()
            if file_lower in FILE_MARKER_TECH_MAP:
                technologies.add(FILE_MARKER_TECH_MAP[file_lower])

            # 2. Capture baseline language using extensions
            _, ext = os.path.splitext(file)
            ext_lower = ext.lower()
            if ext_lower in EXTENSION_TECH_MAP:
                technologies.add(EXTENSION_TECH_MAP[ext_lower])

    # Sorted execution array output for absolute UI determinism and predictability
    return file_count, folder_count, sorted(list(technologies)), tree


async def clone_repository(repo_url: str):
    """
    Orchestrates repository cloning, structural content analysis, 
    automatic vector database indexing, and automated AI summary compilation.
    """
    repo_url = repo_url.split("?")[0]
    print(f"📥 CLONING REPOSITORY INTERFACE TARGET: {repr(repo_url)}")

    repo_name = extract_repo_name(repo_url)
    base_dir = "../data/repositories"
    os.makedirs(base_dir, exist_ok=True)
    repo_path = os.path.join(base_dir, repo_name)

    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    print("⚡ Executing remote Git Clone orchestration...")
    
    try:
        Repo.clone_from(repo_url, repo_path, depth=1)
        print("🚀 Git Clone transaction successfully verified.")
    except Exception as e:
        raise Exception(f"Repository clone failed: {str(e)}")

    # Single-pass analyzer topology walk (Balanced Hybrid Model)
    file_count, folder_count, technologies, tree = process_repository_topology(repo_path)

    # Read physical code blocks safely through updated 1MB reader filters
    code_files = extract_code_files(repo_path)

    print(f"🔄 Syncing code blocks with ChromaDB chunk pipelines...")

    try:
        # Atomic Overwrite: Puraane vectors clear karo taaki stale chunks na rahein
        delete_repo_vectors(repo_name)

        # Chunks process aur embed karke save karo
        save_embeddings(
            repo_name,
            code_files
        )

        print(f"🎯 Vectors fully committed for {repo_name}.")

    except Exception as e:
        print(f"⚠️ ChromaDB Vector Storage Failure: {str(e)}")

    # Extract summaries post-indexing phase
    readme_content = generate_repository_summary(repo_path)
    ai_summary = generate_ai_summary(readme_content)

    return {
        "repo_name": repo_name,
        "repo_path": repo_path,
        "file_count": file_count,
        "folder_count": folder_count,
        "technologies": technologies,
        "tree": tree,
        "summary": ai_summary,
        "code_files": code_files
    }