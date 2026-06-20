import os

ALLOWED_EXTENSIONS = (
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".go",
    ".rs",
    ".php",
    ".cs",
    ".cpp",
    ".cc",
    ".cxx",
    ".c",
    ".h",
    ".hpp",
    ".kt",
    ".swift",
    ".dart"
)

IGNORE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    "dist",
    "build",
    ".next",
    ".nuxt",
    "coverage",
    "target",
    "bin",
    "obj",
    "vendor",
    ".idea",
    ".vscode"
}


def extract_code_files(repo_path):

    code_files = []

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_DIRS
        ]

        for file in files:

            if not file.endswith(ALLOWED_EXTENSIONS):
                continue

            full_path = os.path.join(
                root,
                file
            )

            try:

                with open(
                    full_path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as f:

                    content = f.read()

                # Skip empty files
                if not content.strip():
                    continue

                code_files.append(
                    {
                        "file_path": os.path.relpath(
                            full_path,
                            repo_path
                        ),
                        "content": content,
                        "extension": os.path.splitext(file)[1]
                    }
                )

            except Exception as e:

                print(
                    f"ERROR READING FILE: {full_path}"
                )

                print(str(e))

                continue

    print(
        f"TOTAL CODE FILES FOUND: {len(code_files)}"
    )

    return code_files