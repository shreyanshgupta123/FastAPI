from fastapi import Body,FastAPI

app=FastAPI()

BOOKS = [
    {"title": "Book 1", "author": "Author 1", "year": 2020},
    {"title": "Book 2", "author": "Author 2", "year": 2021},
    {"title": "Book 3", "author": "Author 3", "year": 2022}
]

@app.get("/books/author/{author_name}")
async def get_books_by_author(author_name: str):
    author_books = [book for book in BOOKS if book["author"].casefold() == author_name.casefold()]
    if author_books:
        return author_books
    return {"message": "Books by this author not found"}