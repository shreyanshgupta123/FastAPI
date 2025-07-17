from fastapi import Body, FastAPI

app= FastAPI()

class Book:
    id:str
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id: str, title: str, author: str, description: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

BOOKS=[
    Book("1", "AI/ML", "Author 1", "Description of Book 1", 5),
    Book("2", "Understand Angular", "Author 2", "Description of Book 2", 4),
    Book("3", "Understand React", "Author 3", "Description of Book 3", 3),
    Book("4", "Nural network", "Author 4", "Description of Book 4", 5),
    Book("5", "learn python", "Author 5", "Description of Book 5", 2),
    Book("6", "learn FASTAPI", "Author 6", "Description of Book 6", 4)
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.post("/create_book")
async def create_book(book_request:Body()): # type: ignore
    BOOKS.append(book_request)
    return {"message": "Book created successfully", "book": book_request}


