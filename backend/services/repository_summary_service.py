import os


def generate_repository_summary(repo_path):
    context_parts = []

    # -------------------------
    # README
    # -------------------------

    readme_files = [
        "README.md",
        "README.MD",
        "readme.md",
        "README"
    ]

    readme_found = False

    for file_name in readme_files:

        readme_path = os.path.join(
            repo_path,
            file_name
        )

        if os.path.exists(readme_path):

            with open(
                readme_path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                content = file.read()

            context_parts.append(
                f"README:\n{content[:3000]}"
            )

            readme_found = True
            break

    if not readme_found:

        context_parts.append(
            "README: Not found"
        )

    # -------------------------
    # Repository Structure
    # -------------------------

    structure = []
    file_count = 0

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [
            d for d in dirs
            if d not in {
                ".git",
                "node_modules",
                "__pycache__",
                "dist",
                "build",
                ".next",
                "venv"
            }
        ]

        relative = os.path.relpath(
            root,
            repo_path
        )

        for file in files:

            file_count += 1

            structure.append(
                os.path.join(
                    relative,
                    file
                )
            )

    context_parts.append(
        f"\nTOTAL FILES: {file_count}"
    )

    context_parts.append(
        "\nREPOSITORY STRUCTURE:\n"
        + "\n".join(structure[:200])
    )

    return "\n\n".join(
        context_parts
    )