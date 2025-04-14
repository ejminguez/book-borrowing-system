from . import BaseModel
from . import date

class UserSchema(BaseModel):
    user_id: str
    username: str
    email: str
    hashed_password: str
    is_active: bool = True

class ReaderSchema(BaseModel):
    user_id: str
    role: str

class LibrarianSchema(BaseModel):
    user_id: str
    role: str

class AdminSchema(BaseModel):
    user_id: str
    role: str

class BookSchema(BaseModel):
    book_id: str
    book_title: str
    author: str
    year_published: int
    genre: str

class Borrow_Records_Schema(BaseModel):
    record_id: str
    book_id: str
    user_id: str
    borrow_date: date
    return_date: date
    status: str