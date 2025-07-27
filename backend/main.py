from fastapi import FastAPI
import uvicorn
from models.sentiment_model import SingleRequest, SingleResponse, BatchRequest, BatchResponse
from core.sentiment import analyze_batch, analyze_single
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from core.util.recommender import BookRecommender, Book

app = FastAPI(title="Book Review Sentiment API")
recommender = BookRecommender()

@app.post("/sentiment/single", response_model=SingleResponse)
async def sentiment_single(req: SingleRequest):
    try:
        out = analyze_single(req.review)
        return SingleResponse(review=req.review, label=out.get("label"), score=out.get("score"), error=None)
    except Exception as e:
        return SingleResponse(review=req.review, label=None, score=None, error=str(e))

@app.post("/sentiment/batch", response_model=BatchResponse)
async def sentiment_batch(req: BatchRequest):
    results = analyze_batch(req.reviews)
    return BatchResponse(results=results)

class QueryText(BaseModel):
    query: str

class TitlesList(BaseModel):
    titles: List[str]

# Endpoints
@app.post("/recommend/similar", response_model=List[Book])
async def recommend_similar(payload: QueryText):
    return await recommender.similar_books(payload.query)

@app.post("/recommend/author", response_model=List[Book])
async def recommend_author(payload: QueryText):
    return await recommender.by_author(payload.query)

@app.post("/recommend/genre", response_model=List[Book])
async def recommend_genre(payload: QueryText):
    return await recommender.by_genre(payload.query)

@app.post("/recommend/related", response_model=List[Book])
async def recommend_related(payload: QueryText):
    return await recommender.related_to(payload.query)

@app.post("/recommend/user_preferred", response_model=List[Book])
async def recommend_user_preferred(payload: TitlesList):
    return await recommender.user_preferred(payload.titles)

@app.post("/recommend/content_based", response_model=List[Book])
async def recommend_content_based(payload: QueryText):
    return await recommender.content_based(payload.query)

@app.post("/recommend/collaborative", response_model=List[Book])
async def recommend_collaborative(payload: TitlesList):
    return await recommender.collaborative(payload.titles)

@app.post("/recommend/hybrid", response_model=List[Book])
async def recommend_hybrid(payload: TitlesList):
    return await recommender.hybrid(payload.titles)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)