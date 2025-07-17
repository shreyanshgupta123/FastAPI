from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int
    def __init__(self, id: int, title: str, author: str, description: str, rating: int,published_date:int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date  
class BookRequest(BaseModel):
    id:Optional[int] = Field(description="Book ID, auto-generated if not provided",default=None)
    title: str = Field(min_length=3, max_length=100)
    author: str = Field(min_length=3)
    description: str = Field(min_length=3)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(description="Year of publication", ge=1900, le=2100)
    model_config={
    "json_schema_extra": {
        "example": {
            "title": "Book name",
            "author": "Author Name",
            "description": "Description of the book",
            "rating": 5,
            "published_date": 2023
                }
    }
    }
BOOKS = [
    Book(1, "AI/ML", "Author 1", "Description of Book 1", 5,2020),
    Book(2, "Understand Angular", "Author 2", "Description of Book 2", 4,2021),
    Book(3, "Understand React", "Author 3", "Description of Book 3", 3,2022),
    Book(4, "Neural network", "Author 4", "Description of Book 4", 5, 2023),
    Book(5, "Learn Python", "Author 5", "Description of Book 5", 2, 2024),
    Book(6, "Learn FastAPI", "Author 6", "Description of Book 6", 4, 2025)
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return vars(book)
    return {"error": "Book not found"}

@app.get("/books/")
async def read_book_by_published_date(published_date: int):
    books_by_published_date = [
        vars(book) for book in BOOKS if book.published_date == published_date
    ]
    if not books_by_published_date:
        return {"error": "No books found with the specified publication year"}
    return books_by_published_date

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            deleted_book = BOOKS.pop(i)
            return {"message": "Book deleted successfully", "book": vars(deleted_book)}
   

@app.put("/books/update_book")
async def update_book(book_request: BookRequest):
    for book in range(len(BOOKS)):
        if BOOKS[book].id == book_request.id:
            BOOKS[book]=book_request
            print(BOOKS[book])
            return {"message": "Book updated successfully", "book": vars(BOOKS[book])}
    return {"error": "Book not found"}

@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    new_book = assign_book_id(new_book)
    BOOKS.append(new_book)
    return {"message": "Book created successfully", "book": vars(new_book)}

def assign_book_id(book: Book):
    if BOOKS:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book
