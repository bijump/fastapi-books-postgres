from fastapi import FastAPI
import schemas
import models
from database import Base,engine

app=FastAPI()
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)
@app.get("/")
def get_root():
    return {"book":"Hello","price":120}
@app.get("/{id}")
def get_root_id(id:int):
    return {"id":{id},"book":"Hello","price":120}

@app.post("/book/")
def create_book(request:schemas.BookAuthor):
    models.add_book(convert_into_book_db(request.book),convert_into_author_db(request.author))
    return("<Book(Book:{0},Author:{1})> ".format(request.book.title,request.author.first_name))

def convert_into_book_db(book:schemas.Book):
    return models.Book(title=book.title,number_of_pages=book.number_of_pages)
def convert_into_author_db(author:schemas.Author):
    return models.Author(first_name=author.first_name,last_name=author.last_name)