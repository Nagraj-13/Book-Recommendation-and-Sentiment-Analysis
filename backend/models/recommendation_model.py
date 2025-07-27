from pydantic import BaseModel, Field
from typing import Optional


class Book(BaseModel):
    title: str = Field(..., description="Book title")
    author: str = Field(..., description="Author name")
    genre: str = Field(..., description="Genre of the book")
    description: Optional[str] = Field(None, description="Short description")
    publication_year: Optional[int] = Field(None, description="Year of publication")
    rating: Optional[float] = Field(None, description="Rating out of 5")