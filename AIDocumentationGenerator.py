import os
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

class DocumentationGenerator:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Falta la API key de OpenAI")
        self.client = OpenAI(api_key=api_key)
    
    def generate_docstring(self, function_code: str) -> str:
        """Genera docstring automático para una función."""
        prompt = f"""
Analiza la siguiente función Python y genera un docstring completo 
en formato Google Style que incluya:
- Descripción breve y detallada
- Parámetros con tipos
- Valor de retorno
- Excepciones que puede lanzar
- Ejemplo de uso

Función:
{function_code}
"""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",   # usa gpt-4o-mini (más rápido y económico que gpt-4)
            messages=[
                {"role": "system", "content": "Eres un experto en documentación de código Python."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.3
        )
        
        content: Optional[str] = response.choices[0].message.content
        return content or ""
    
    def generate_readme(self, project_info: str) -> str:
        """Genera README.md automático para un proyecto."""
        prompt = f"""
Crea un README.md profesional para el siguiente proyecto:
{project_info}

Incluye:
- Título y descripción
- Instalación
- Uso básico
- API Reference
- Contribuciones
- Licencia

Usa formato Markdown con badges y estructura profesional.
"""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un experto en documentación técnica."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.4
        )
        
        content: Optional[str] = response.choices[0].message.content
        return content or ""

#🚀 Cómo usarla

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
docgen = DocumentationGenerator()

func_code = """
def suma(a: int, b: int) -> int:
    return a + b
"""

print(docgen.generate_docstring(func_code))

print(docgen.generate_readme("Proyecto para demostrar generación automática de documentación"))