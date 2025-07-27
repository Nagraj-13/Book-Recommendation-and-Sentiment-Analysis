from typing import List, Dict
from .util.utill import groq_sentiment_batch, groq_sentiment_single


def analyze_single(review: str) -> Dict[str, float]:
    result = groq_sentiment_single(review=review)
    return result

def analyze_batch(reviews: List[str]) -> List[Dict]:
    results: List[Dict] = []
    for start in range(0, len(reviews), 25):
        chunk = reviews[start : start + 25]
        try:
            batch_out = groq_sentiment_batch(chunk)

            for item in batch_out:
                results.append({
                    "review": item.get("review"),
                    "label": item.get("label"),
                    "score": item.get("score"),
                    "error": None
                })

        except Exception as e:
            for rev in chunk:
                results.append({
                    "review": rev,
                    "label": None,
                    "score": None,
                    "error": str(e)
                })
    return results
