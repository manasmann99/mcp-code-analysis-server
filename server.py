from fastapi import FastAPI
from pydantic import BaseModel

from tools.analyze import analyze_code
from tools.smells import detect_code_smells
from tools.suggest import suggest_refactoring
from tools.apply import apply_refactoring

app = FastAPI(title="MCP Code Analysis Server")

class CodeRequest(BaseModel):
    code: str

@app.get("/")
def root():
    return {"status": "MCP Server Running"}

@app.post("/analyze")
def analyze(req: CodeRequest):
    return analyze_code(req.code)

@app.post("/smells")
def smells(req: CodeRequest):
    return detect_code_smells(req.code)

@app.post("/suggest")
def suggest(req: CodeRequest):
    return suggest_refactoring(req.code)

@app.post("/apply")
def apply(req: CodeRequest):
    return apply_refactoring(req.code)
