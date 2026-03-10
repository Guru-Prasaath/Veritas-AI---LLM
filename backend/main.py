from fastapi import FastAPI
from pydantic import BaseModel
from ai_engine import analyze_text

app = FastAPI()

class NewsInput(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "Veritas AI backend running"}


@app.post("/analyze")
async def analyze(news: NewsInput):
    result = analyze_text(news.text)
    return result