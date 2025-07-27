from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, confloat, RootModel


class SingleRequest(BaseModel):
    review: str

class SingleResponse(BaseModel):
    review: str
    label: Optional[str]
    score: Optional[float]
    error: Optional[str]

class BatchRequest(BaseModel):
    reviews: List[str]

class BatchResponseItem(BaseModel):
    review: str
    label: Optional[str]
    score: Optional[float]
    error: Optional[str]

class BatchResponse(BaseModel):
    results: List[BatchResponseItem]
    
    
class SentimentLabel(str, Enum):
    VERY_POSITIVE = "Very Positive"
    POSITIVE      = "Positive"
    NEUTRAL       = "Neutral"
    NEGATIVE      = "Negative"
    VERY_NEGATIVE = "Very Negative"

class ReviewSentiment(BaseModel):
    review: str = Field(..., description="The text of the book review")
    label: SentimentLabel = Field(..., description="Sentiment category")
    score: confloat(ge=-1.0, le=1.0) = Field(
        ..., 
        description="Compound sentiment score between -1.0 and 1.0",
        example=0.75
    )
    
class ReviewSentimentList(BaseModel):
   results: List[ReviewSentiment]