import json
from typing import Any, Dict, Optional
from backend.config import OPENAI_API_KEY, OPENAI_MODEL

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY) if (OpenAI and OPENAI_API_KEY) else None

    @property
    def enabled(self): return self.client is not None

    def ask(self, prompt: str) -> str:
        if not self.client:
            return ""
        response = self.client.responses.create(model=OPENAI_MODEL, input=prompt)
        return response.output_text or ""

    def ask_json(self, prompt: str) -> Optional[Dict[str, Any]]:
        text = self.ask(prompt)
        if not text: return None
        try: return json.loads(text)
        except json.JSONDecodeError:
            start, end = text.find("{"), text.rfind("}")
            if start >= 0 and end > start:
                try: return json.loads(text[start:end+1])
                except json.JSONDecodeError: return None
        return None

ai_service = AIService()
