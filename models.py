import enum
from datetime import datetime
from sqlalchemy import(
    Column,
    Integer,
    String,
    Text,
    DateTime,
    CheckConstraint,Enum
)
from database import Base

class Genre(str,enum.Enum):
    roman = "roman"
    story = "hikoya"
    drama = "drama"

class Book(Base):
    __tablename__ = 'books'

    book_id = Column('id',Integer,primary_key=True,nullable=False)
    title = Column(String(length=30),nullable=False)
    auther = Column(String(length=30),nullable=False)
    description = Column(Text)
    pages = Column(Integer,CheckConstraint("pages >= 1"),nullable=False)
    genre = Column(Enum(Genre),nullable=False)

    created_at = Column('created_at',DateTime,default=datetime.now)
    updated_at = Column('updated_at',DateTime,onupdate=datetime.now)