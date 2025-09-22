import os
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AICodeReviewer:
    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Falta la variable OPENAI_API_KEY en .env")
        self.client = OpenAI(api_key=api_key)

    def review_code(self, code: str, language: str = "python") -> str:
        prompt = f"""
Realiza un code review detallado del siguiente código {language}.
Analiza:

1. 🛡️ Seguridad: Vulnerabilidades potenciales
2. 🎯 Performance: Optimizaciones posibles
3. 📖 Legibilidad: Claridad del código
4. 🏗️ Arquitectura: Patrones y estructuras
5. 🧪 Testing: Cobertura y casos edge
6. 📏 Estándares: PEP 8, mejores prácticas

Código:
{code}

Proporciona sugerencias específicas y ejemplos de mejora.
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",  # más rápido y barato que gpt-4
            messages=[
                {"role": "system", "content": "Eres un senior developer experto en code review."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.3
        )

        content: Optional[str] = response.choices[0].message.content
        return content or ""
    
# 🚀 Uso del revisor    
if __name__ == "__main__":
    reviewer = AICodeReviewer()
    code_to_review = """
def suma(a, b):
    return a+b
"""
    print(reviewer.review_code(code_to_review))