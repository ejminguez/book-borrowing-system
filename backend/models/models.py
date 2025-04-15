from sqlalchemy import Column, Date, String, ForeignKey, text, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from enum import Enum
from database import Base

class RoleEnum(str, Enum):
    reader = "reader"
    librarian = "librarian"
    admin = "admin"

class StatusEnum(str, Enum):
    borrowed = "borrowed"
    returned = "returned"
    lost = "lost"
    damaged = "damaged"

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(String, default=True)
    role = Column(SQLAlchemyEnum(RoleEnum, name="role_enum"), nullable=False, default=RoleEnum.reader)

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
    status = Column(SQLAlchemyEnum(StatusEnum, name="status_enum"), nullable=False, default=StatusEnum.borrowed)