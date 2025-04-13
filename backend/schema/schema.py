class User(BaseModel):
    user_id: str
    username: str
    email: str
    hashed_password: str
    is_active: bool = True

class Reader(BaseModel):
    user_id: str
    role: str

class Librarian(BaseModel):
    user_id: str
    role: str

class Admin(BaseModel):
    user_id: str
    role: str

class Book(BaseModel):
    book_id: str
    book_title: str
    author: str
    year_published: int
    genre: str

class Borrow_Records(BaseModel):
    record_id: str
    book_id: str
    user_id: str
    borrow_date: str
    return_date: str
    status: str