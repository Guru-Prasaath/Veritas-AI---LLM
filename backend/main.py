from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.ai_engine import analyze_text


# Initialize FastAPI app
app = FastAPI(
    title="Veritas AI API",
    description="AI-powered misinformation detection system using RAG + LLM",
    version="1.0.0"
)


# Request schema
class NewsInput(BaseModel):
    text: str


# Root endpoint (health check)
@app.get("/")
def home():
    return {
        "message": "Veritas AI backend running",
        "status": "ok"
    }


# Analyze endpoint
@app.post("/analyze")
async def analyze(news: NewsInput):

    try:

        # Basic validation
        if not news.text or len(news.text.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Input text cannot be empty"
            )

        # Run AI pipeline
        analysis = analyze_text(news.text)

        return {
            "status": "success",
            "analysis": analysis
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )