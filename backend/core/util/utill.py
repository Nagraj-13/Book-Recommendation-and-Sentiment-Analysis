import os
from groq import Groq
from typing import List, Dict
import json
from models.sentiment_model import ReviewSentiment, ReviewSentimentList
from dotenv import load_dotenv
import os

# 1) load .env into environment
load_dotenv()  

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama3-70b-8192" 
def groq_sentiment_single(review: str) -> Dict[str, float]:
    """
    Sends a single review to the Groq model and returns the sentiment analysis result.
    """
    prompt = f"""
You are a sentiment analysis API. ONLY return a valid JSON in the following format:

{{
  "review": "<original review text>",
  "label": "Very Negative | Negative | Neutral | Positive | Very Positive",
  "score": float between -1.0 and 1.0
}}

Review: "{review}"
"""

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        response_format={"type": "json_object"}
    )

    return json.loads(resp.choices[0].message.content.strip())

def groq_sentiment_batch(reviews: List[str]) -> List[Dict]:
    prompt = f"""
You are a sentiment analysis API. ONLY return a valid JSON in the following format:

{{
  "reviews": [
    {{
      "review": "<text>",
      "label": "Very Negative | Negative | Neutral | Positive | Very Positive",
      "score": float between -1.0 and 1.0
    }}
  ]
}}

Reviews:
""" + "\n".join([f"- {review}" for review in reviews])

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        response_format={"type": "json_object"}
    )

    raw = json.loads(resp.choices[0].message.content.strip())

    return raw["reviews"]
