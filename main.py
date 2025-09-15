from typing import Annotated
from enum import Enum
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from database import Base, engine, Session
from models import Book

app = FastAPI(title="NT-Kutubxona")

Base.metadata.create_all(engine)


# --- READ bitta kitob ---
@app.get("/api/books/{book_id}")
def get_book_detail(
    book_id: Annotated[int, Path(title="bitta kitob id si", ge=1, le=1000)]
):
    db = Session()
    result = db.query(Book).filter(Book.book_id == book_id).first()
    if result:
        return {
            "id": result.book_id,
            "title": result.title,
            "desciption": result.description,
            "auther": result.auther,
            "genre": result.genre,
            "pages": result.pages,
        }
    raise HTTPException(status_code=404, detail="Bunday kitob mavjud emas")


# --- READ user ---
@app.get("/api/users/{username}")
def get_user_detail(
    username: Annotated[str, Path(min_length=5, max_length=30, pattern='^[a-z0-9_-]{5,30}$')]
):
    return {"username": username}


# --- READ kitoblar listi ---
@app.get("/api/books/")
def get_book_list(
    auther: Annotated[str, Query(title="kitob muallifi", min_length=5, max_length=30)]
):
    db = Session()
    results = db.query(Book).filter(Book.auther == auther).all()
    return results


# --- ENUM janr ---
class Genre(str, Enum):
    roman = "roman"
    story = "hikoya"
    drama = "drama"


# --- REQUEST BODY modeli ---
class BookCreate(BaseModel):
    title: Annotated[str, Field(title="Kitob nomi", min_length=5, max_length=30)]
    auther: Annotated[str, Field(title="kitob muallifi", min_length=5, max_length=30)]
    pages: Annotated[int, Field(title="Varoqlar soni", ge=1, le=1000)]
    description: Annotated[str | None, Field(default=None, title="tarif")] = None
    genre: Genre


# --- CREATE kitob ---
@app.post("/api/books/")
def create_book(book_data: BookCreate):
    db = Session()
    book = Book(
        title=book_data.title,
        auther=book_data.auther,
        pages=book_data.pages,
        description=book_data.description,
        genre=book_data.genre,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return {"message": "Kitob qo'shildi", "book_id": book.book_id}


# --- UPDATE kitob (PUT) ---
@app.put("/api/books/{book_id}")
def update_book(book_id: int, book_data: BookCreate):
    db = Session()
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")

    book.title = book_data.title
    book.auther = book_data.auther
    book.pages = book_data.pages
    book.description = book_data.description
    book.genre = book_data.genre

    db.commit()
    db.refresh(book)
    return {"message": "Kitob yangilandi", "book": book.book_id}


# --- PATCH (faqat qisman o‘zgartirish) ---
@app.patch("/api/books/{book_id}")
def patch_book(book_id: int, book_data: dict):
    db = Session()
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")

    for key, value in book_data.items():
        if hasattr(book, key):
            setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return {"message": "Kitob qisman yangilandi", "book": book.book_id}


# --- DELETE kitob ---
@app.delete("/api/books/{book_id}")
def delete_book(book_id: int):
    db = Session()
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")

    db.delete(book)
    db.commit()
    return {"message": "Kitob o‘chirildi", "book_id": book_id}
