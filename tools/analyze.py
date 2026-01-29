import ast

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.classes = []
        self.methods = []
        self.imports = set()
        self.complexity = 0

    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.functions.append(node.name)
        self.complexity += 1
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                self.methods.append(f"{node.name}.{item.name}")
        self.generic_visit(node)

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_Try(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.add(node.module)


def analyze_code(code: str):
    try:
        tree = ast.parse(code)
        analyzer = CodeAnalyzer()
        analyzer.visit(tree)

        return {
            "lines_of_code": len(code.splitlines()),
            "functions": analyzer.functions,
            "classes": analyzer.classes,
            "methods": analyzer.methods,
            "imports": sorted(analyzer.imports),
            "cyclomatic_complexity": analyzer.complexity
        }

    except SyntaxError as e:
        return {
            "error": "Invalid Python code",
            "details": str(e)
        }
