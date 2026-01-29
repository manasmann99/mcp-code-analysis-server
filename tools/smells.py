import ast
from collections import defaultdict


def detect_code_smells(code: str):
    smells = []

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {"smells": ["Invalid Python syntax"]}

    # ---------- 1. Long Method (>50 lines) ----------
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.end_lineno and (node.end_lineno - node.lineno) > 50:
                smells.append(f"Long method (>50 lines): {node.name}")

    # ---------- 2. Too Many Parameters (>5) ----------
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if len(node.args.args) > 5:
                smells.append(f"Too many parameters (>5): {node.name}")

    # ---------- 3. Deep Nesting (>3 levels) ----------
    def max_depth(node, depth=0):
        if not list(ast.iter_child_nodes(node)):
            return depth
        return max(max_depth(child, depth + 1) for child in ast.iter_child_nodes(node))

    if max_depth(tree) > 6:  # ~3 nested blocks
        smells.append("Deep nesting (>3 levels)")

    # ---------- 4. Duplicate Code Blocks ----------
    blocks = defaultdict(int)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            normalized_body = "".join(ast.dump(stmt) for stmt in node.body)
            blocks[normalized_body] += 1

    if any(count > 1 for count in blocks.values()):
        smells.append("Duplicate code blocks detected")

    # ---------- 5. Dead Code / Unused Imports ----------
    imports = set()
    used = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                imports.add(name.name)
        elif isinstance(node, ast.ImportFrom):
            for name in node.names:
                imports.add(name.name)
        elif isinstance(node, ast.Name):
            used.add(node.id)

    unused = imports - used
    if unused:
        smells.append(f"Unused imports detected: {', '.join(unused)}")

    return {"smells": smells}
