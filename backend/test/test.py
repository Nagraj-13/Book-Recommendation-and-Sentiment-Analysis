from google import genai
from pydantic import BaseModel
import asyncio
from pydantic import BaseModel, Field
from typing import List, Optional, Union

class BookRec(BaseModel):
    title: str
    author: str
    publised_at: str
    genre:str
     
class Book(BaseModel):
    """
    A Pydantic model to represent a book with its key details. This structure
    will be enforced on the JSON output from the Gemini API.
    """
    title: str = Field(description="The full title of the book.")
    author: str = Field(description="The author or authors of the book.")
    genre: str = Field(description="The primary genre of the book (e.g., Science Fiction, Fantasy, Biography).")
    description: str = Field(description="A concise, one or two-sentence summary of the book's plot or main theme.")
    publication_year: Optional[int] = Field(None, description="The year the book was first published.")
    rating: Optional[float] = Field(None, description="A hypothetical rating for the book out of 5, reflecting its general acclaim.")

client = genai.Client(api_key='')
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="List and recommend the books, for the provided book or title or genre. {Rich Dad Poor Dad}",
    config={
        "response_mime_type": "application/json",
        "response_schema": list[Book],
    },
)
# Use the response as a JSON string.
print(response.text)

# Use instantiated objects.
my_recipes: list[BookRec] = response.parsed

async def get_book_recommendations(prompt: str, num_books: int) -> List[Book]:
    """
    A generic helper function to get book recommendations from the Gemini API.

    Args:
        prompt (str): The detailed prompt to send to the model.
        num_books (int): The number of books requested (used for error logging).

    Returns:
        A list of Pydantic Book objects, or an empty list if an error occurs.
    """
    try:
        # Use generate_content_async for asynchronous calls.
        response = await client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                # CORRECTION: Pass the Pydantic type directly for the schema.
                # This is the modern and recommended approach.
                "response_schema": List[Book],
            },
        )
        # CORRECTION: Use the '.parsed' attribute to get the Pydantic objects.
        # This avoids manual JSON loading and validation.
        return response.text
    except Exception as e:
        print(f"An error occurred while generating {num_books} recommendations: {e}")
        return []

async def recommend_similar_books_by_keywords(query: str, num_books: int = 3) -> List[Book]:
    """Recommends books similar to a given book name, title, or keywords."""
    prompt = (
        f"Recommend {num_books} books that are similar in theme, style, or content to '{query}'. "
        "Provide the title, author, genre, a one-sentence description, publication year, and a hypothetical rating for each."
    )
    return await get_book_recommendations(prompt, num_books)

async def get_books_by_author(author_name: str, num_books: int = 3) -> List[Book]:
    """Returns a list of books written by a specific author."""
    prompt = (
        f"List {num_books} popular or representative books written by the author '{author_name}'. "
        "For each book, provide the title, author, genre, a one-sentence description, publication year, and a hypothetical rating."
    )
    return await get_book_recommendations(prompt, num_books)

async def get_top_books_by_genre(genre: str, num_books: int = 3) -> List[Book]:
    """Returns a list of top or highly-regarded books within a specific genre."""
    prompt = (
        f"List {num_books} highly-regarded or popular books in the '{genre}' genre. "
        "For each book, provide the title, author, genre, a one-sentence description, publication year, and a hypothetical rating."
    )
    return await get_book_recommendations(prompt, num_books)

async def hybrid_recommendation(
    seed_input: Union[str, List[str]],
    recommendation_type: str = "book_title",
    num_books: int = 3
) -> List[Book]:
    """
    Provides a hybrid recommendation by combining aspects of content-based and
    collaborative-based approaches.
    """
    prompt_prefix = ""
    if recommendation_type == "book_title" and isinstance(seed_input, str):
        prompt_prefix = (
            f"Considering the book '{seed_input}', recommend books that are a mix of "
            "closely related titles (e.g., in the same series or with similar themes) and books that readers "
            "who enjoyed this book also frequently liked."
        )
    elif recommendation_type == "genre" and isinstance(seed_input, str):
        prompt_prefix = (
            f"For the genre '{seed_input}', recommend books that are a mix of "
            "top-rated titles and those with unique but appealing content features within that genre."
        )
    elif recommendation_type == "author" and isinstance(seed_input, str):
        prompt_prefix = (
            f"For the author '{seed_input}', recommend books that include other works by them "
            "and books by different authors that share a similar writing style or thematic focus."
        )
    elif recommendation_type == "user_profile":
        pref_str = ", ".join(seed_input) if isinstance(seed_input, list) else seed_input
        prompt_prefix = (
            f"Based on a user who likes '{pref_str}', recommend books "
            "that combine content similarity with what other readers with similar tastes have enjoyed."
        )
    else:
        print("Invalid recommendation_type or seed_input for hybrid recommendation.")
        return []

    prompt = (
        f"{prompt_prefix} Recommend {num_books} books. For each, provide the title, author, "
        "genre, a one-sentence description, publication year, and a hypothetical rating."
    )
    return await get_book_recommendations(prompt, num_books)


# 4. Example Usage
async def main():
    """Main function to demonstrate the recommendation utilities."""
    print("--- 📚 Book Recommendation Examples 📚 ---\n")

    print("--- 1. Books by Author: 'Brandon Sanderson' ---")
    author_books = await get_books_by_author("Brandon Sanderson", num_books=2)
    for book in author_books:
        print(f"  - {book.title} ({book.publication_year}) by {book.author} [{book.genre}] - Rating: {book.rating}/5")
        print(f"    Description: {book.description}\n")

    print("--- 2. Top Books by Genre: 'Cyberpunk' ---")
    genre_books = await get_top_books_by_genre("Cyberpunk", num_books=2)
    for book in genre_books:
        print(f"  - {book.title} ({book.publication_year}) by {book.author} [{book.genre}] - Rating: {book.rating}/5")
        print(f"    Description: {book.description}\n")

    print("--- 3. Hybrid Recommendation for a Book: 'Project Hail Mary' ---")
    hybrid_rec = await hybrid_recommendation("Project Hail Mary", recommendation_type="book_title", num_books=2)
    for book in hybrid_rec:
        print(f"  - {book.title} ({book.publication_year}) by {book.author} [{book.genre}] - Rating: {book.rating}/5")
        print(f"    Description: {book.description}\n")


if __name__ == "__main__":
    # Ensure you have set your GOOGLE_API_KEY environment variable
    # before running this script.
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Failed to run the main async loop. Ensure your API key is configured. Error: {e}")
