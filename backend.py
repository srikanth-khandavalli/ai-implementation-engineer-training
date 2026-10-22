import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)
app = FastAPI(title="AI Extraction Microservice")

# Input Schema
class ExtractionRequest(BaseModel):
    raw_text: str = Field(..., min_length=10, description="Raw bio or text to process")

# Output Schema
class ExtractedEntities(BaseModel):
    name: str
    company: str
    experience_years: int
    skills: list[str]

@app.post("/extract", response_model=ExtractedEntities, status_code=status.HTTP_200_OK)
async def extract_details(payload: ExtractionRequest):
    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Extract professional details from: {payload.raw_text}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ExtractedEntities,
                temperature=0.0,
            ),
        )
        return ExtractedEntities.model_validate_json(response.text)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference pipeline failed: {str(exc)}"
        )