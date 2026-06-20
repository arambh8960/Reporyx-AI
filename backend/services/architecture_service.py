import os
from collections import Counter

def analyze_architecture(repo_path):
    blueprint = {
        "repository_status": "Active",
        "dominant_extensions": {},
        "largest_directories": [],
        "system_entry_points": [],
        "build_and_configurations": [],
        "core_implementation_layers": [],
        "communication_layers": [],
        "presentation_and_ui_layers": [],
        "utility_and_shared_layers": []
    }

    ignore_dirs = {".git", "node_modules", "__pycache__", "dist", "build", ".next", "venv", ".env", "target", "out", ".idea", ".vscode", ".cargo", "vendor", ".gradle"}
    
    universal_config_patterns = {"package.json", "package-lock.json", "requirements.txt", "pyproject.toml", "poetry.lock", "go.mod", "go.sum", "cargo.toml", "cargo.lock", "composer.json", "pom.xml", "build.gradle", "settings.gradle", "cmakelists.txt", "makefile", "gemfile", "mix.exs", "docker-compose.yml", "dockerfile", "vagrantfile", ".env.example", "tsconfig.json", "webpack.config.js", "vite.config.ts", "rollup.config.js"}
    universal_entry_patterns = {"main.py", "app.py", "manage.py", "wsgi.py", "asgi.py", "index.js", "server.js", "index.ts", "server.ts", "main.go", "app.go", "main.rs", "lib.rs", "program.cs", "app.cs", "application.java", "main.java", "application.kt", "main.cpp", "main.c", "index.php", "main.zig", "main.sh"}

    core_keywords = {"src", "core", "lib", "library", "internal", "pkg", "package", "services", "domain", "engine", "compiler", "logic"}
    communication_keywords = {"api", "routes", "route", "controllers", "controller", "handlers", "endpoints", "middleware", "grpc", "proto", "cli", "commands", "rpc", "abi"}
    ui_keywords = {"ui", "frontend", "components", "pages", "views", "styles", "assets", "public", "static", "terminal", "gui"}
    utility_keywords = {"utils", "helpers", "shared", "common", "tools", "extensions", "infrastructure", "db", "database", "models", "migrations", "config"}

    global_extension_counter = Counter()
    directory_volume_registry = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        relative = os.path.relpath(root, repo_path)
        is_root = (relative == ".")

        for file in files:
            file_lower = file.lower()
            file_path = os.path.join(relative, file) if not is_root else file
            
            if file_lower in universal_config_patterns: blueprint["build_and_configurations"].append(file_path)
            if file_lower in universal_entry_patterns: blueprint["system_entry_points"].append(file_path)
            ext = os.path.splitext(file_lower)[1]
            if ext: global_extension_counter[ext] += 1

        if is_root: continue

        path_parts = [part.lower() for part in relative.split(os.sep)]
        if len(files) > 0:
            directory_volume_registry.append({"directory": relative, "file_count": len(files)})

        if any(ck in path_parts for ck in communication_keywords): blueprint["communication_layers"].append({"directory": relative})
        if any(uk in path_parts for uk in ui_keywords): blueprint["presentation_and_ui_layers"].append({"directory": relative})
        if any(utk in path_parts for utk in utility_keywords): blueprint["utility_and_shared_layers"].append({"directory": relative})
        if any(core_k in path_parts for core_k in core_keywords): blueprint["core_implementation_layers"].append({"directory": relative})

    blueprint["dominant_extensions"] = dict(global_extension_counter.most_common(15))
    directory_volume_registry.sort(key=lambda x: x["file_count"], reverse=True)
    blueprint["largest_directories"] = directory_volume_registry[:10]

    return blueprint