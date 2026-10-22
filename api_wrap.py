import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()

client = genai.Client()
app = FastAPI(title="LLM Prompt & Extraction Microservice")

# 1. Request Contract
class ExtractionRequest(BaseModel):
    raw_text: str = Field(..., min_length=10, description="Raw input text to process")
    temperature: float = Field(default=0.0, ge=0.0, le=1.0)

# 2. Response Contract
class ExtractedResponse(BaseModel):
    name: str
    company: str
    experience_years: int
    skills: list[str]

# 3. Async POST Route
@app.post("/extract", response_model=ExtractedResponse, status_code=status.HTTP_200_OK)
async def extract_info(payload: ExtractionRequest):
    try:
        # Crucial teaching point: await client.aio does not block the ASGI worker
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Extract structured details from: {payload.raw_text}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ExtractedResponse,
                temperature=payload.temperature,
            ),
        )
        return ExtractedResponse.model_validate_json(response.text)

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {str(exc)}"
        )