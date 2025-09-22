# AI Development Assistant

![OpenAI](https://img.shields.io/badge/OpenAI-API-blue)
![Python](https://img.shields.io/badge/Python-3.11%2B-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-teal)

## Descripción

AI Development Assistant es una suite de herramientas basadas en IA para asistir a desarrolladores en la generación de código, revisión automática, detección de bugs, generación de documentación y creación de tests. Utiliza modelos avanzados de OpenAI, Antropic, Google y está construido sobre FastAPI para ofrecer endpoints RESTful.

## Instalación

1. Crear el entorno virtual y activar:
   ```sh
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```
3. Configura tu archivo `.env` con la variable `OPENAI_API_KEY`:
   ```
   OPENAI_API_KEY=tu_clave_openai
   ```

## Uso Básico

Levanta la API con FastAPI:
```sh
uvicorn api_dev_assistant:app --reload
```

Accede a la documentación interactiva en [http://localhost:8000/docs](http://localhost:8000/docs).

Levanta el Fontend:
```sh
streamlit run front-end-ia.py
```

Accede a la ejecución de entorno en [http://localhost:8501](http://localhost:8501).


## API Reference

### Generación de Código
- **POST** `/api/v1/generate-code`
  - Request: `prompt`, `language`, `provider`
  - Response: Código generado, proveedor, tokens usados, tiempo de ejecución

### Revisión de Código
- **POST** `/api/v1/review-code`
  - Request: `code`, `language`
  - Response: Revisión automática del código

### Generación de Tests
- **POST** `/api/v1/generate-tests`
  - Request: `code`, `framework`
  - Response: Tests automáticos generados

### Detección de Bugs
- Usa la clase [`AIBugDetector`](AIBugDetector.py) para analizar errores y optimizar código.

### Generación de Documentación
- Usa la clase [`DocumentationGenerator`](AIDocumentationGenerator.py) para crear documentación y README.md automáticos.

## Estructura del Proyecto

```
.env
AIBugDetector.py
AICodeAssistant.py
AICodeReviewer.py
AIDocumentationGenerator.py
TestGenerator.py
api_dev_assistant.py
front-end-ia.py
README.md
requirements.txt
styles/
typings/
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para sugerencias y mejoras.

## Licencia

Este proyecto está bajo la licencia MIT.

---

> Generado automáticamente con [`AIDocumentationGenerator.generate_readme`](DocumentationGenerator.py)