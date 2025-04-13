from sqlalchemy import Column, Date, String, ForeignKey, text
from . import Base
from database import engine
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(String, default=True)  # Changed to String to match the schema

class Reader(Base):
    __tablename__ = "readers"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    role = Column(String, default="reader")

class Librarian(Base):
    __tablename__ = "librarians"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    role = Column(String, default="librarian")

class Admin(Base):
    __tablename__ = "admins"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    role = Column(String, default="admin")

class Book(Base):
    __tablename__ = "books"

    book_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), nullable=False)
    book_title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year_published = Column(Date, nullable=False)
    genre = Column(String, nullable=False)

class Borrow_Records(Base):
    __tablename__ = "borrow_records"

    record_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), nullable=False)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.book_id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    borrow_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    status = Column(String, default="borrowed")  # Changed to String to match the schema