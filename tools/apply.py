import ast
import textwrap

class UnusedImportRemover(ast.NodeTransformer):
    def __init__(self):
        self.used_names = set()

    def visit_Name(self, node):
        self.used_names.add(node.id)
        return node

    def visit_Import(self, node):
        kept = []
        for alias in node.names:
            if alias.asname or alias.name in self.used_names:
                kept.append(alias)
        return ast.Import(names=kept) if kept else None

    def visit_ImportFrom(self, node):
        kept = []
        for alias in node.names:
            if alias.asname or alias.name in self.used_names:
                kept.append(alias)
        return ast.ImportFrom(module=node.module, names=kept, level=node.level) if kept else None


def apply_refactoring(code: str):
    try:
        tree = ast.parse(code)

        # Collect used identifiers
        remover = UnusedImportRemover()
        remover.visit(tree)

        # Remove unused imports
        tree = remover.visit(tree)
        ast.fix_missing_locations(tree)

        # Format code consistently
        refactored = ast.unparse(tree)

        return {
            "refactored_code": textwrap.dedent(refactored).strip(),
            "applied_refactors": [
                "Removed unused imports",
                "Formatted code consistently"
            ]
        }

    except SyntaxError as e:
        return {
            "error": "Invalid Python code",
            "details": str(e)
        }
