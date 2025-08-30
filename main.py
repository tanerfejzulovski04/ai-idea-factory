from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import logging

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()

class Topic(BaseModel):
    topic: str = Field(..., min_length=4, description="The blog topic (required, non-empty)")

# Request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info("Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logging.info("Response status: {response.status_code}")
    return response

# POST /generate-ideas
@app.post("/generate-ideas")
async def generate_ideas(data: Topic):
    try:
        resp = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages= [
                {
                    "role": "user",
                    "content": "Give me 5 blog post ideas about" + data.topic + ". Only output the ideas, no introduction or explanation."}
            ]
        )
        return {"ideas": resp.choices[0].message.content.split("\n")}
    except Exception as e:
        error_json = e.response.json()
        message = error_json.get("error", {}).get("message", "Unknown error")
        return JSONResponse(status_code=404, content={"error": message})

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "OK"}

# Use /static/index.html for UI
@app.get("/")
async def root():
    return FileResponse("static/index.html", headers={"Cache-Control": "no-store"})

app.mount("/static", StaticFiles(directory="static"), name="static")