# api_dev_assistant.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import os
from dotenv import load_dotenv

# Aquí importamos las clases que ya definiste en otros archivos
from AICodeAssistant import AICodeAssistant
from AICodeReviewer import AICodeReviewer
from TestGenerator import TestGenerator

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title="AI Development Assistant API",
    description="API para asistencia de desarrollo con IA",
    version="1.0.0"
)

# ---------------------------
# Modelos Pydantic
# ---------------------------
class CodeRequest(BaseModel):
    prompt: str
    language: str = "python"
    provider: str = "openai"

class CodeResponse(BaseModel):
    generated_code: str
    provider_used: str
    tokens_used: int
    execution_time: float

class ReviewRequest(BaseModel):
    code: str
    language: str = "python"

class TestRequest(BaseModel):
    code: str
    framework: str = "pytest"

# ---------------------------
# Endpoints
# ---------------------------
@app.post("/api/v1/generate-code", response_model=CodeResponse)
async def generate_code(request: CodeRequest):
    """Genera código usando IA"""
    try:
        assistant = AICodeAssistant()
        start_time = asyncio.get_event_loop().time()
        generated_code = assistant.generate_code(request.prompt, request.language)
        end_time = asyncio.get_event_loop().time()

        return CodeResponse(
            generated_code=generated_code,
            provider_used=request.provider,
            tokens_used=len(generated_code.split()),
            execution_time=end_time - start_time
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/review-code")
async def review_code(request: ReviewRequest):
    """Realiza code review usando IA"""
    try:
        reviewer = AICodeReviewer()
        review = reviewer.review_code(request.code, request.language)
        return {"review": review, "status": "completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/generate-tests")
async def generate_tests(request: TestRequest):
    """Genera tests automáticos"""
    try:
        generator = TestGenerator(api_key)
        tests = generator.generate_tests(request.code, request.framework)
        return {"tests": tests, "framework": request.framework}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
