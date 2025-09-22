import os
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AICodeAssistant:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("Falta la variable OPENAI_API_KEY en el archivo .env")
        self.client = OpenAI(api_key=api_key)
    
    def generate_code(self, prompt: str, language: str = "python") -> str:
        system_prompt = f"""
        Eres un desarrollador experto en {language}.
        Genera código limpio, bien documentado y siguiendo mejores prácticas.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.3
        )
        
        content: Optional[str] = response.choices[0].message.content
        return content or ""

# Uso del asistente
if __name__ == "__main__":
    assistant = AICodeAssistant()
    code = assistant.generate_code("Crea una función que valide emails usando regex")
    print(code)
