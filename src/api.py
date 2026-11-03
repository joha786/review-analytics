from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine

BASE = Path(__file__).resolve().parent.parent

app = FastAPI(title="Review Analytics API")
model = joblib.load(BASE / "src" / "model.joblib")
engine = create_engine(f"sqlite:///{BASE / 'reviews.db'}")


class Review(BaseModel):
    text: str


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(review: Review):
    if not review.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    return {"sentiment": model.predict([review.text])[0]}


@app.get("/sentiment-trend")
def sentiment_trend():
    sql = """
        SELECT strftime('%Y-%m', date) AS month, sentiment, COUNT(*) AS total
        FROM reviews
        GROUP BY month, sentiment
        ORDER BY month
    """
    return pd.read_sql(sql, engine).to_dict("records")


@app.get("/top-products")
def top_products(limit: int = 10):
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 100")
    sql = """
        SELECT ProductId, COUNT(*) AS total_reviews,
               ROUND(AVG(Score), 2) AS avg_rating
        FROM reviews
        GROUP BY ProductId
        ORDER BY total_reviews DESC
        LIMIT :limit
    """
    df = pd.read_sql(sql, engine, params={"limit": limit})
    return df.to_dict("records")