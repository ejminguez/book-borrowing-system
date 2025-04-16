from . import BaseModel
from . import date

class RoleEnumSchema(BaseModel):
    reader: str = "reader"
    librarian: str = "librarian"
    admin: str = "admin"

class StatusEnumSchema(BaseModel):
    borrowed: str = "borrowed"
    returned: str = "returned"
    lost: str = "lost"
    damaged: str = "damaged"

class UserSchema(BaseModel):
    username: str
    email: str
    is_active: bool = True
    role: str

class BookSchema(BaseModel):
    book_title: str
    author: str
    year_published: str
    copies_available: int = 1

class GenreSchema(BaseModel):
    genre_name: str

class Book_Genre_Schema(BaseModel):
    book_id: str
    genre_id: int

class Borrow_Records_Schema(BaseModel):
    book_id: str
    user_id: str
    borrow_date: date
    return_date: date
    status: str