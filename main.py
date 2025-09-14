from typing import Annotated
from enum import Enum
from fastapi import FastAPI,Path,Query
from pydantic import BaseModel,Field
from database import Base,engine
from models import Book


app = FastAPI(title="NT-Kutubxon")

Base.metadata.create_all(engine)


@app.get("/api/books/{book_id}")
def get_book_detail(
    #book_id:int = Path(title = "bitta kitob idsi",ge=1,le=100)
    book_id: Annotated[int,Path(title="bitta kitob id si",ge=1,le=1000)]
):
    return {"book":book_id}



@app.get("/api/users/{username}")
def get_user_detail(
    #username  :str = Path(min_length=5,max_length=30)
    username: Annotated[str,Path(min_length=5,max_length=30,pattern='^[a-z0-9_-]{5,30}')]

    ):
    return{"username":username}

@app.get("/api/books/")
def get_book_list(
    #auther: str = Query(title="kitob muallifi",min_length=5,max_length=30)
    auther: Annotated[str,Query(title="kitob muallifi",min_length=5,max_length=30)]
):
    return {"auther":auther}


class Genre(str,Enum):
    roman = "roman"
    story = "hikoya"
    drama = "drama"




class Book(BaseModel):
    #title:       str = Field(min_length=5,max_length=30)
    title:        Annotated[str,Field(title="Kitob nomi",min_length=5,max_length=30)]
    #auther:      str  = Field(title="Kitob muallifi",min_length=5,max_length=30)
    auther:       Annotated[str,Field(title="kitb muallif",min_length=5,max_length=30)]
    #pages:       int   = Field(title="Varoqlar soni",ge=1,le=1000)
    pages:        Annotated[int,Field(title="Varoqlar soni",ge=1,le=1000)]
    #description: str | None = Field(default=None,title="tarifi")
    description:  Annotated[str | None,Field(default=None,title="tarif")] = None
    genre:        Genre


@app.post("/api/books/")
def create_book(
    book:Book
):
    print(book.model_dump())
    return {}



