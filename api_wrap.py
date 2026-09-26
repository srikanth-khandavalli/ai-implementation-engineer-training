import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not configured in .env")

client = genai.Client(api_key=api_key)
app = FastAPI(title="LLM Prompt & Extraction Microservice")

# 1. Request Contract
class ExtractionRequest(BaseModel):
    raw_text: str = Field(..., min_length=10, description="Raw input text to process")
    temperature: float = Field(default=0.0, ge=0.0, le=1.0)

# 2. Response Contract
class ExtractedEntities(BaseModel):
    name: str
    company: str
    experience_years: int
    skills: list[str]

# 3. Async POST Route
@app.post("/extract", response_model=ExtractedEntities, status_code=status.HTTP_200_OK)
async def extract_info(payload: ExtractionRequest):
    try:
        # Crucial teaching point: await client.aio does not block the ASGI worker
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Extract structured details from: {payload.raw_text}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ExtractedEntities,
                temperature=payload.temperature,
            ),
        )
        return ExtractedEntities.model_validate_json(response.text)

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {str(exc)}"
        )