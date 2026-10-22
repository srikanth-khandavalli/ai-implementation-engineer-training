from dotenv import load_dotenv
from google import genai
from google.genai import types
from fastapi import FastAPI
from pydantic import BaseModel, Field

load_dotenv()
client = genai.Client()

app = FastAPI(title="AI Extraction Microservice")

class ExtractionRequest(BaseModel):
    raw_text: str = Field(..., min_length=10, description="Raw Bio to process")

class ExtractedEntities(BaseModel):
    name: str
    company: str
    experience_yts: int
    skills: list[str]

@app.post("/extract")
async def extract_details(payload:ExtractionRequest):
    response=await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Extract Professional details from: {payload.raw_text}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ExtractedEntities,
            temperature=0.0
        )
    )
    return ExtractedEntities.model_validate_json(response.text)