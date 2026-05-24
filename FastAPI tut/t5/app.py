from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import database

# Initialize the database
database.init_db()

app = FastAPI()

# ======================================================
# PYDANTIC MODELS
# ======================================================

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

# ======================================================
# API ROUTES
# ======================================================

@app.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    """
    Registers a new user in the database.
    """
    db_user = database.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    user_id = database.create_user(user.username, user.password)
    return {"id": user_id, "username": user.username}

@app.post("/login")
def login(user: UserCreate):
    """
    Verifies user credentials.
    """
    db_user = database.authenticate_user(user.username, user.password)
    
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful", "username": db_user["username"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
