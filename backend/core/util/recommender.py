
import os
import asyncio
from typing import List, Optional
from google import genai
from pydantic import BaseModel, Field
from models.recommendation_model import Book
from dotenv import load_dotenv
import os


load_dotenv('../../.env')  
# Pydantic models
title_recommendation = List[str]

class BookRecommender:
    def __init__(self: Optional[str] = None):
        key = os.getenv('GEMINI_API_KEY')
        if not key:
            raise RuntimeError('Falied in Loading the model')
        self.client = genai.Client(api_key=key)

    async def _generate(self, prompt: str, schema: type[list[Book]]) -> List[Book]:
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": schema,
            },
        )
        # blocking call; wrap in executor if needed
        return response.parsed  # type: ignore

    async def similar_books(self, query: str) -> List[Book]:
        prompt = f"List books similar to '{query}' with title, author, genre, description"
        return await self._generate(prompt, list[Book])

    async def by_author(self, author: str) -> List[Book]:
        prompt = f"List books written by author '{author}'"
        return await self._generate(prompt, list[Book])

    async def by_genre(self, genre: str) -> List[Book]:
        prompt = f"Top books in the genre '{genre}'"
        return await self._generate(prompt, list[Book])

    async def related_to(self, title: str) -> List[Book]:
        prompt = f"Most related books to '{title}'"
        return await self._generate(prompt, list[Book])

    async def user_preferred(self, titles: List[str]) -> List[Book]:
        joined = ", ".join(titles)
        prompt = f"Recommend books based on user's purchased list: {joined}"
        return await self._generate(prompt, list[Book])

    async def content_based(self, text: str) -> List[Book]:
        prompt = f"Content-based recommendations for: {text}"
        return await self._generate(prompt, list[Book])

    async def collaborative(self, purchased: List[str]) -> List[Book]:
        joined = ", ".join(purchased)
        prompt = f"Collaborative filtering recommendations based on: {joined}"
        return await self._generate(prompt, list[Book])

    async def hybrid(self, purchased: List[str]) -> List[Book]:
        joined = ", ".join(purchased)
        prompt = f"Hybrid recommendations (content + collaborative) based on: {joined}"
        return await self._generate(prompt, list[Book])
