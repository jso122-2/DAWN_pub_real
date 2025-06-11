# Re-run the import dependency map scan scoped to core DAWN subdirectories
import os
scan_targets = ["core", "bloom", "owl", "pulse", "mycelium", "router", "semantic"]
import ast

def map_imports_scoped(directories):
    dependency_map = {}
    for folder in directories:
        for subdir, _, files in os.walk(folder):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(subdir, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            tree = ast.parse(f.read(), filename=path)
                        imports = []
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for n in node.names:
                                    imports.append(n.name)
                            elif isinstance(node, ast.ImportFrom):
                                imports.append(f"{node.module or ''}.{'.'.join([n.name for n in node.names])}".strip("."))

                        rel_path = os.path.relpath(path, ".").replace("\\", "/")
                        dependency_map[rel_path] = sorted(set(imports))

                    except Exception as e:
                        dependency_map[path] = [f"# Error parsing: {e}"]

    return dependency_map

scoped_deps = map_imports_scoped(scan_targets)

# Write results to diagnostics
scoped_map_path = "diagnostics/dependency_map_scoped.txt"
with open(scoped_map_path, "w") as f:
    for module, imports in scoped_deps.items():
        f.write(f"{module}:\n")
        for imp in imports:
            f.write(f"  - {imp}\n")
        f.write("\n")

scoped_map_path
