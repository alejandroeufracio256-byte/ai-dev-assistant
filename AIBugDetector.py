import os
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AIBugDetector:
    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Falta la variable OPENAI_API_KEY en .env")
        self.client = OpenAI(api_key=api_key)

    def analyze_error(self, error_msg: str, code_snippet: str) -> str:
        """Analiza errores y propone soluciones con ejemplos corregidos."""
        prompt = f"""
Analiza el siguiente error y código. Proporciona:

1. 🔍 Causa del error
2. 💡 Solución paso a paso
3. 🛠️ Código corregido
4. 🚀 Mejoras adicionales
5. 📚 Recursos de aprendizaje

Error: {error_msg}

Código:
{code_snippet}

Sé específico y educativo en las explicaciones.
"""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",  # más rápido y barato que gpt-4
            messages=[
                {"role": "system", "content": "Eres un experto en debugging y resolución de problemas."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.2
        )
        content: Optional[str] = response.choices[0].message.content
        return content or ""

    def optimize_performance(self, code: str) -> str:
        """Sugiere optimizaciones de performance y benchmarks esperados."""
        prompt = f"""
Analiza este código y sugiere optimizaciones específicas:

🎯 Análisis de Performance:
- Complejidad temporal actual
- Bottlenecks identificados
- Uso de memoria
- Algoritmos más eficientes

📈 Optimizaciones:
- Versión optimizada del código
- Explicación de mejoras
- Benchmarks esperados

Código:
{code}
"""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un experto en optimización de algoritmos y performance."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.3
        )
        content: Optional[str] = response.choices[0].message.content
        return content or ""

#🚀 Ejemplo de uso

if __name__ == "__main__":
    detector = AIBugDetector()

    # Ejemplo 1: analizar error
    error_msg = "NameError: name 'x' is not defined"
    code = "print(x)"
    print(detector.analyze_error(error_msg, code))

    # Ejemplo 2: optimizar código
    slow_code = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
"""
    print(detector.optimize_performance(slow_code))
