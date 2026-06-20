import re

GLOBAL_CONTROL_KEYWORDS = {
    "if", "else", "elif", "for", "while", "do", "switch", "case", "catch", "try", 
    "finally", "return", "throw", "assert", "import", "require", "export", "package", 
    "using", "include", "print", "println", "console", "log", "await", "async", "yield",
    "const", "let", "var", "public", "private", "protected", "static", "final", "void",
    "int", "float", "double", "char", "bool", "string", "long", "short", "interface", "type"
}

ROUTE_METHODS = {"get", "post", "put", "delete", "patch", "use"}

def extract_code_entities(files):
    entities = []
    method_pattern = (r'(?:(?:public|private|protected|static|final|virtual|override)\s+)*'
                      r'(?:[\w<>\[\]]+\s+)+'
                      r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(')

    handler_patterns = [
        r'(?:export\s+)?(?:async\s+)?(?:def|function|fn|func)\s+([a-zA-Z_][a-zA-Z0-9_]*)',
        r'(?:const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=',
        method_pattern
    ]

    for file in files:
        content = file.get("content", "")
        file_path = file.get("file_path", "")
        functions = []
        current_function = None
        classes, imports, routes = set(), set(), []
        
        lines = content.splitlines()
        for i, line in enumerate(lines):
            line_s = line.strip()
            if not line_s or line_s.startswith(("//", "#", "/*", "*", "-->", ";")): continue

            # 1. Imports & Classes
            import_match = re.search(r'(?:from|import|require|include|using)\s+(?:\{[^}]*\}\s+from\s+)?[\'"]?([a-zA-Z0-9_\.\/\<\>]+)', line_s)
            if import_match: imports.add(import_match.group(1))
            class_match = re.search(r'(?:class|struct|interface|type)\s+([a-zA-Z_][a-zA-Z0-9_]*)', line_s)
            if class_match: classes.add(class_match.group(1))

            # 2. Function/Method Detection (Patched)
            match = re.search(r'(?:export\s+)?(?:async\s+)?(?:function|def|fn|func)\s+([a-zA-Z_][a-zA-Z0-9_]*)', line_s) or \
                    re.search(r'(?:const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*.*=>', line_s) or \
                    re.search(method_pattern, line_s)
            
            if match and match.group(1).lower() not in GLOBAL_CONTROL_KEYWORDS:
                current_function = {"name": match.group(1), "calls": []}
                functions.append(current_function)
                continue 

            # 3. Route Extraction
            std_route = re.search(r'\.(get|post|put|delete|patch|use)\s*\(\s*[\'"]([^\'"]+)[\'"]\s*,\s*([a-zA-Z_][a-zA-Z0-9_]*)', line_s)
            dec_route = re.search(r'@.*\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'"]+)', line_s, re.IGNORECASE)
            spr_route = re.search(r'@(GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping)\s*\(\s*[\'"]([^\'"]+)', line_s)

            if std_route:
                routes.append({"method": std_route.group(1).upper(), "path": std_route.group(2), "handler": std_route.group(3)})
            elif dec_route or spr_route:
                found_handler = "unknown"
                for j in range(i + 1, min(i + 6, len(lines))):
                    for pattern in handler_patterns:
                        h_match = re.search(pattern, lines[j])
                        if h_match and h_match.group(1).lower() not in GLOBAL_CONTROL_KEYWORDS:
                            found_handler = h_match.group(1)
                            break
                    if found_handler != "unknown": break
                method = dec_route.group(1).upper() if dec_route else spr_route.group(1).replace("Mapping", "").upper()
                path = dec_route.group(2) if dec_route else spr_route.group(2)
                routes.append({"method": method, "path": path, "handler": found_handler})

            # 4. Call Extraction
            if current_function:
                possible_calls = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', line_s)
                for call in possible_calls:
                    if call.lower() not in GLOBAL_CONTROL_KEYWORDS and call.lower() not in ROUTE_METHODS and call != current_function["name"]:
                        if call not in current_function["calls"]: current_function["calls"].append(call)

        entities.append({"file_path": file_path, "functions": functions, "classes": sorted(list(classes)), "imports": sorted(list(imports)), "routes": routes})
    return entities