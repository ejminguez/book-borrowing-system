# Book Borrowing System

## 📝 Description
I created this project to practice RBAC (Role-Based Access Control). \
There are 3 roles: reader, librarian, and admin.

## 🛠️ Technology Stack
- FastAPI
- Supabase database
- Vite + React

## ✨ Features

#### Reader
Readers can only do the following:
```
- see all books
- borrow books
```

#### Librarian
Librarians can only do the following:
```
- see all books
- give permission when readers borrow books
```

#### Admins
Admins can only do the following:
```
- see all books
- add books
- delete books
- update books
- ban readers
- fire librarians
```
