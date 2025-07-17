from fastapi import FastAPI,Path,Query,HTTPException
from typing import Optional
from pydantic import BaseModel, Field
from starlette import status
app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id:Optional[int] = Field(description="Book ID, auto-generated if not provided",default=None)
    title: str = Field(min_length=3, max_length=100)
    author: str = Field(min_length=3)
    description: str = Field(min_length=3)
    rating: int = Field(gt=-1, lt=6)
    model_config={
    "json_schema_extra": {
        "example": {
            "title": "Book name",
            "author": "Author Name",
            "description": "Description of the book",
            "rating": 5
                }
    }
    }
BOOKS = [
    Book(1, "AI/ML", "Author 1", "Description of Book 1", 5),
    Book(2, "Understand Angular", "Author 2", "Description of Book 2", 4),
    Book(3, "Understand React", "Author 3", "Description of Book 3", 3),
    Book(4, "Neural network", "Author 4", "Description of Book 4", 5),
    Book(5, "Learn Python", "Author 5", "Description of Book 5", 2),
    Book(6, "Learn FastAPI", "Author 6", "Description of Book 6", 4)
]

@app.get("/books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def read_book(book_id: int=Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return vars(book)
        raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/",status_code=status.HTTP_200_OK)
async def read_book_by_rating(rating: int=Query(gt=-1, lt=6)):
    books_by_rating = [vars(book) for book in BOOKS if book.rating == rating]
    if not books_by_rating:
        return {"error": "No books found with the specified rating"}
    return books_by_rating

@app.delete("/books/{book_id}",status_code=status.HTTP_200_OK)
async def delete_book(book_id: int=Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            deleted_book = BOOKS.pop(i)
            book_changed = True
            return {"message": "Book deleted successfully", "book": vars(deleted_book)}
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book Does not exist")

@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_request: BookRequest):
    for book in range(len(BOOKS)):
        if BOOKS[book].id == book_request.id:
            BOOKS[book]=book_request
            print(BOOKS[book])
            return {"message": "Book updated successfully", "book": vars(BOOKS[book])}
    return {"error": "Book not found"}

@app.post("/create-book",status_code=status.HTTP_201_CREATED)
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

