from app.ollama_client import call_llm
import json

def extract_json(text: str):
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return None

    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None


def suggest_refactoring(code: str):
    base_prompt = f"""
You are an API that returns STRICT JSON.

Rules:
- Output ONLY valid JSON
- No markdown
- No explanations
- No code blocks
- No extra text

Schema (must be filled):

{{
  "suggestions": [
    {{
      "issue": "string",
      "reason": "string",
      "before": "string",
      "after": "string"
    }}
  ]
}}

Analyze and refactor this code:

{code}
"""

    raw = call_llm(base_prompt)
    parsed = extract_json(raw)

    # 🔁 Retry once if model misbehaves
    if not parsed:
        retry_prompt = f"""
Your previous response was INVALID.

Return ONLY VALID JSON matching this schema and NOTHING ELSE.

{{
  "suggestions": [
    {{
      "issue": "string",
      "reason": "string",
      "before": "string",
      "after": "string"
    }}
  ]
}}

Code:
{code}
"""
        raw = call_llm(retry_prompt)
        parsed = extract_json(raw)

    if parsed:
        return parsed

    # 🔥 Final safe fallback (never crash API)
    return {
        "suggestions": [],
        "warning": "LLM failed to return structured JSON",
        "raw_response": raw
    }
