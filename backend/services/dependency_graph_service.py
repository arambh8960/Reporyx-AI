import re


IMPORT_PATTERNS = {
    ".py": [
        r"import\s+([\w\.]+)",
        r"from\s+([\w\.]+)\s+import"
    ],

    ".js": [
        r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]',
        r'require\([\'"](.+?)[\'"]\)'
    ],

    ".jsx": [
        r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]',
        r'require\([\'"](.+?)[\'"]\)'
    ],

    ".ts": [
        r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]'
    ],

    ".tsx": [
        r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]'
    ],

    ".java": [
        r'import\s+([\w\.]+);'
    ],

    ".go": [
        r'import\s+"([^"]+)"'
    ],

    ".rs": [
        r'use\s+([\w:]+)'
    ],

    ".php": [
        r'use\s+([\w\\]+);'
    ],

    ".cs": [
        r'using\s+([\w\.]+);'
    ]
}


def extract_imports(content, extension):

    imports = set()

    patterns = IMPORT_PATTERNS.get(
        extension,
        []
    )

    for pattern in patterns:

        matches = re.findall(
            pattern,
            content,
            re.MULTILINE
        )

        for match in matches:

            if isinstance(match, tuple):
                match = match[0]

            imports.add(match)

    return list(imports)


def build_dependency_graph(code_files):

    nodes = []
    edges = []

    for file in code_files:

        file_path = file["file_path"]

        extension = file.get(
            "extension",
            ""
        )

        content = file["content"]

        nodes.append(file_path)

        imports = extract_imports(
            content,
            extension
        )

        for imported in imports:

            edges.append(
                {
                    "source": file_path,
                    "target": imported,
                    "type": "import"
                }
            )

    return {
        "nodes": nodes,
        "edges": edges
    }