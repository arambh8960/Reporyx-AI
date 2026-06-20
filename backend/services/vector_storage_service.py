from database.chroma_db import collection
from services.embedding_service import generate_embedding
from services.chunking_service import create_chunks

def delete_repo_vectors(repo_name):
    """
    Deletes all existing vectors for a repository to ensure clean overwrites.
    """
    try:
        collection.delete(
            where={
                "repo_name": repo_name
            }
        )
        print(f"🧹 DELETED CHROMA VECTORS FOR {repo_name}")
    except Exception as e:
        # Failure here won't crash the pipeline anymore thanks to upsert downstream
        print(f"⚠️ Warning: Safe delete failed for {repo_name}: {str(e)}")


def save_embeddings(repo_name, code_files):
    """
    Converts chunked code files into embedded vectors and upserts them to ChromaDB
    with synchronized tracking coordinates for semantic layout reconstruction.
    """
    ids = []
    documents = []
    embeddings = []
    metadatas = []

    vector_count = 0

    for file in code_files:
        # Generates structured dict chunks: {"chunk_index": x, "start_line": y, "end_line": z, "content": "..."}
        chunks = create_chunks(file["content"])

        for chunk in chunks:
            # Synchronized naming interface using the true chunk token index
            chunk_id = (
                f"{repo_name}_"
                f"{file['file_path']}_"
                f"{chunk['chunk_index']}"
            )

            # Fix 1: Extracting string content before entering embedding engine pipeline
            embedding = generate_embedding(chunk["content"])

            ids.append(chunk_id)
            documents.append(chunk["content"])
            embeddings.append(embedding)

            # Fix 2: Schema mapping matching retrieval sorting layer queries ("chunk_index")
            metadatas.append(
                {
                    "repo_name": repo_name,
                    "file_path": file["file_path"],
                    "chunk_index": chunk["chunk_index"],
                    "start_line": chunk["start_line"],
                    "end_line": chunk["end_line"]
                }
            )

            vector_count += 1

    # Fix 3: Idempotent transactional commit to prevent duplicate ID crashes
    if ids:
        collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    print("🚀 TOTAL VECTORS SAVED =", vector_count)