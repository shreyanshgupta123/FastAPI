from fastapi import Body,FastAPI

app=FastAPI()

BOOKS = [
    {"title": "Book 1", "author": "Author 1", "year": 2020},
    {"title": "Book 2", "author": "Author 2", "year": 2021},
    {"title": "Book 3", "author": "Author 3", "year": 2022}
]

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/books")
async def get_books():
    return BOOKS

# @app.get("/books/{dynamic_params}")
# async def get_book(dynamic_params):
#     return {"Dynamic params": dynamic_params}


@app.get("/books/mybooks{title}")
async def get_book(title: str):
    for book in BOOKS:
        if book["title"].casefold() == title.casefold():
            print(f"Found book: {book}")
            return book
    return {"message": "Book not found"}

@app.get("/books/")
async def get_book(author: str, year: int):
    auth_books = []
    for book in BOOKS:
        if book["author"].casefold() == author.casefold() or book.get("year") == year:
            auth_books.append(book)
    if auth_books:
        return auth_books
    return {"message": "Book not found"}

#POST
@app.post("/books/create_Books")
async def create_book(new_books=Body()):
    BOOKS.append(new_books)
    return {"message": "Book created successfully", "book": new_books}

#PUT
@app.put("/books/update_Books")
async def update_book(update_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i]["title"].casefold() == update_book["title"].casefold():
            BOOKS[i] = update_book
            return {"message": "Book updated successfully", "book": update_book}
        

#Delete
@app.delete("/books/delete_Books/{title}")
async def delete_book(title: str):
    for i in range(len(BOOKS)):
        if(BOOKS[i].get("title").casefold() == title.casefold()):
            BOOKS.pop(i)
            return {"message": "Book deleted successfully"}
        

@app.get("/books/author/{author_name}")
async def get_books_by_author(author_name: str):
    author_books = [book for book in BOOKS if book["author"].casefold() == author_name.casefold()]
    if author_books:
        return author_books
    return {"message": "Books by this author not found"}
