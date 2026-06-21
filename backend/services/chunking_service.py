import re

def create_chunks(content: str, chunk_size: int = 150, overlap: int = 50) -> list[dict]:
    """
    Advanced Syntax-Aware Chunker v3.5 for Reporyx-AI.
    Optimizations:
    - Language-agnostic context tracking (Supports functions as parent contexts).
    - Deduplication Filter: Context injection is completely skipped for the 1st chunk (Index 0)
      or if the chunk already starts exactly at the boundary declaration.
    """
    if not content or not content.strip():
        return []

    if chunk_size <= overlap:
        raise ValueError("chunk_size must be strictly greater than overlap.")

    lines = content.splitlines()
    total_lines = len(lines)
    chunks = []
    chunk_index = 0
    start = 0

    # 1. Broad structural declaration matches
    STANDARD_BOUNDARY = re.compile(
        r'^\s*(def|class|function|func|interface|struct|enum|contract|module|trait|namespace|fn|package)\b'
        r'|^\s*(public|private|protected|export|default)\s+(class|interface|enum|void|struct|record|type|\w+)\b'
    )
    COMPLEX_BOUNDARY = re.compile(
        r'^\s*(type\s+\w+\s+struct|impl\s+\w+|object\s+\w+|protocol\s+\w+|record\s+\w+)'
    )

    def is_boundary(line_str: str) -> bool:
        return bool(STANDARD_BOUNDARY.match(line_str) or COMPLEX_BOUNDARY.match(line_str))

    boundary_lines = [i for i, line in enumerate(lines) if is_boundary(line)]

    while start < total_lines:
        ideal_end = start + chunk_size
        actual_end = ideal_end

        if ideal_end < total_lines:
            lookback_limit = max(start + overlap, ideal_end - overlap)
            possible_boundaries = [b for b in boundary_lines if lookback_limit <= b <= ideal_end + 10]

            if possible_boundaries:
                actual_end = possible_boundaries[-1]
            else:
                actual_end = ideal_end

        if actual_end <= start:
            actual_end = ideal_end

        chunk_lines = lines[start:actual_end]
        raw_content = "\n".join(chunk_lines).strip()

        if raw_content:
            parent_context = ""
            
            # Optimization 2 Check: Only compute context if we are past chunk 0 
            # AND the chunk doesn't organically start on a boundary line itself.
            if chunk_index > 0 and start not in boundary_lines:
                # Scan backward to find the absolute closest structural scope (Class or Function)
                for i in range(start, -1, -1):
                    if is_boundary(lines[i]):
                        # Optimization 1 Fix: No keyword filter here, any valid boundary acts as parent
                        parent_context = f"// Context: {lines[i].strip()}\n"
                        break

            final_content = parent_context + raw_content if parent_context else raw_content

            chunks.append({
                "chunk_index": chunk_index,
                "start_line": start + 1,
                "end_line": min(actual_end, total_lines),
                "content": final_content
            })
            chunk_index += 1

        actual_chunk_length = actual_end - start
        dynamic_overlap = min(overlap, actual_chunk_length // 3)
        
        advance_by = max(actual_chunk_length - dynamic_overlap, 1)
        start += advance_by

    return chunks