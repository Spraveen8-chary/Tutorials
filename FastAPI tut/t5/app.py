"""
========================================================
            FastAPI Database (SQLAlchemy)
========================================================

Scenario:
---------
You need to store user data permanently. You want to register new users 
and verify their passwords during login.

Topic:
------
1. SQLAlchemy Integration
2. Sync vs Async DB calls
3. CRUD Operations (Create, Read, Update, Delete)

What it is used for:
--------------------
Connecting your API to a database (like SQLite, PostgreSQL, or MySQL) 
using an Object-Relational Mapper (ORM).

Problem it solves:
------------------
Keeps data alive after the server restarts. Using an ORM like SQLAlchemy 
allows you to interact with the database using Python objects instead 
of raw SQL strings.

How it is different from Flask:
-------------------------------
1. Dependency Injection: FastAPI uses a `get_db` dependency to handle 
   database sessions. This ensures connections are opened and closed 
   correctly for every request.
2. Modern SQLAlchemy: FastAPI works great with SQLAlchemy 2.0 and 
   native async drivers, making it much faster for high-concurrency apps.
3. Pydantic Models: We use Pydantic to validate the data coming in 
   (Request) and the data going out (Response), keeping it separate 
   from the DB model.

Run:
----
uvicorn app:app --reload

========================================================
"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# ======================================================
# 1. DATABASE SETUP (SQLite)
# ======================================================

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# 'check_same_thread=False' is needed ONLY for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ======================================================
# 2. DB MODEL (How data is stored)
# ======================================================

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String) # In real apps, ALWAYS hash passwords!

# Create the tables
Base.metadata.create_all(bind=engine)

# ======================================================
# 3. PYDANTIC MODELS (How data is validated)
# ======================================================

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

# ======================================================
# 4. DEPENDENCY
# ======================================================

def get_db():
    """
    Creates a new DB session for each request and closes it after.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ======================================================
# 5. API ROUTES
# ======================================================

app = FastAPI()

@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user in the database.
    """
    # Check if user exists
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = UserDB(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    """
    Verifies user credentials.
    """
    db_user = db.query(UserDB).filter(
        UserDB.username == user.username, 
        UserDB.password == user.password
    ).first()
    
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful", "username": db_user.username}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
