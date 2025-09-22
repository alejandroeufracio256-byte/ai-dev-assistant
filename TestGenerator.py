import os
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class TestGenerator:
    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Falta la variable OPENAI_API_KEY en .env")
        self.client = OpenAI(api_key=api_key)

    def generate_tests(self, code: str, framework: str = "pytest") -> str:
        """Genera tests automáticos para un fragmento de código"""
        prompt = f"""
Genera un archivo de tests en {framework} para el siguiente código Python.
Incluye:
- Casos básicos
- Casos edge
- Pruebas negativas
- Comentarios sobre cobertura

Código:
{code}
"""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",  # más barato y rápido que gpt-4
            messages=[
                {"role": "system", "content": "Eres un experto en testing de software con Python."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3
        )
        content = response.choices[0].message.content
        return content or ""
