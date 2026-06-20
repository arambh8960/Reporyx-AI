from database.chroma_db import collection
from services.embedding_service import generate_embedding

async def retrieve_relevant_files(repo_name, question, max_token_budget=15000):
    """
    Universally retrieves, aggregates, and prioritizes code chunks from ChromaDB.
    Relies purely on vector mathematical similarity and continuous context aggregation.
    
    Fully secure against duplicate token budget leaks and null metadata runtime exceptions.
    """
    # 1. Generate Query Vector and fetch expanded high-recall sample space
    question_embedding = generate_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=50,  # Improved broad recall limits balanced by downstream filters
        where={"repo_name": repo_name}
    )

    # Guard clause for empty result matrixes
    if not results or "documents" not in results or not results["documents"] or not results["documents"][0]:
        return []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # 2. Extract and Aggregate by File Target (Pure Mathematical Bundling)
    aggregated_files = {}

    for doc, metadata, distance in zip(documents, metadatas, distances):
        # Production Bug Fix: Prevent crashes if ChromaDB records hold null/None metadatas
        metadata = metadata or {}
        file_path = metadata.get("file_path", "unknown_file")
        
        try:
            chunk_index = int(metadata.get("chunk_index", 0))
        except (ValueError, TypeError):
            chunk_index = 0
        
        chunk_density = max(1, len(doc) // 4)

        chunk_payload = {
            "content": doc,
            "score": float(distance),
            "tokens": chunk_density,
            "chunk_index": chunk_index
        }

        if file_path not in aggregated_files:
            aggregated_files[file_path] = {
                "file_path": file_path,
                "best_score": chunk_payload["score"],
                "total_tokens": chunk_payload["tokens"],
                "chunks": [chunk_payload]
            }
        else:
            aggregated_files[file_path]["chunks"].append(chunk_payload)
            aggregated_files[file_path]["total_tokens"] += chunk_payload["tokens"]
            
            if chunk_payload["score"] < aggregated_files[file_path]["best_score"]:
                aggregated_files[file_path]["best_score"] = chunk_payload["score"]

    # 3. Sort structural components purely based on Vector Similarity Score (No Bias)
    sorted_files = list(aggregated_files.values())
    sorted_files.sort(key=lambda x: x["best_score"])

    # 4. Token Budget Guard & Payload Compiler Loop
    final_retrieved_payload = []
    accumulated_tokens = 0

    print("\n🚀 UNIVERSAL VECTOR RETRIEVAL & AGGREGATION SYSTEM:\n")

    for file_data in sorted_files:
        # Strict Deduplication of overlapping text fragments
        seen_chunks = set()
        unique_chunks = []
        
        for chunk in file_data["chunks"]:
            if chunk["content"] not in seen_chunks:
                seen_chunks.add(chunk["content"])
                unique_chunks.append(chunk)
                
        file_data["chunks"] = unique_chunks

        # Recalculate true token density post-deduplication to clear leakage
        file_data["total_tokens"] = sum(chunk["tokens"] for chunk in file_data["chunks"])

        # Sort internal chunks by sequential index to preserve layout flow
        file_data["chunks"].sort(key=lambda x: (x["chunk_index"], x["score"]))

        # Construct unified continuous content sequence from aggregated chunks
        merged_content_blocks = [c["content"] for c in file_data["chunks"]]
        unified_content = "\n\n// --- [Continuous Context Fragment] ---\n\n".join(merged_content_blocks)

        # Budget Check: Safeguard next operational elements from spilling over max_token_budget
        if accumulated_tokens + file_data["total_tokens"] > max_token_budget:
            if not final_retrieved_payload:
                max_slice = max_token_budget * 4
                unified_content = unified_content[:max_slice] + "\n... [Context truncated due to size constraints]"
                file_data["total_tokens"] = max_token_budget
            else:
                print(f"⚠️ Budget saturated. Slicing lower priority asset: {file_data['file_path']}")
                continue

        accumulated_tokens += file_data["total_tokens"]

        compiled_node = {
            "file_path": file_data["file_path"],
            "content": unified_content,
            "score": round(file_data["best_score"], 4),
            "chunk_count": len(file_data["chunks"])
        }
        
        final_retrieved_payload.append(compiled_node)
        print(f"✅ BUNDLED: {compiled_node['file_path']} => Vector Score: {compiled_node['score']} (Chunks Merged: {compiled_node['chunk_count']})")

        # Updated limit to 8
        if len(final_retrieved_payload) >= 8:
            break

    # Telemetry debugger block
    print(f"\n📊 TOTAL TOKENS USED: {accumulated_tokens} / {max_token_budget}\n")

    return final_retrieved_payload