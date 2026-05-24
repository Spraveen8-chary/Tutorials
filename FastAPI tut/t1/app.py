"""
========================================================
                FastAPI Routing & Validation
========================================================

Scenario:
---------
You are building the foundation of a web API. You need to handle different 
types of requests (Home, Health check) and accept user input via the URL 
path and query parameters.

Topic:
------
1. Basic Routing
2. Path Parameters (with Type Hints)
3. Query Parameters (with Defaults)
4. Automatic Data Validation
5. Automatic Documentation (Swagger/ReDoc)

What it is used for:
--------------------
Mapping URLs to Python functions and ensuring the data sent by users 
is in the correct format (e.g., an ID must be an integer).

Problem it solves:
------------------
In traditional frameworks, you often have to manually convert strings to 
integers or check if a "name" was provided. FastAPI does this automatically 
using Python Type Hints.

How it is different from Flask:
-------------------------------
1. Type Safety: Flask uses converters in the route string (`<int:id>`). 
   FastAPI uses standard Python type hints in the function signature (`id: int`).
2. Auto-Docs: FastAPI automatically creates a `/docs` (Swagger) and `/redoc` 
   page. Flask requires extra plugins for this.
3. Validation: If you send a string to an `int` parameter, FastAPI returns a 
   clear 422 error automatically. Flask would either 404 or require manual error handling.

Run:
----
uvicorn app:app --reload

Test URLs:
----------
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/greet?name=Praveen
- http://127.0.0.1:8000/user/Praveen
- http://127.0.0.1:8000/post/10
- http://127.0.0.1:8000/docs (The Interactive API Documentation)

========================================================
"""

from fastapi import FastAPI
from typing import Optional

# Create FastAPI application
app = FastAPI()

# ======================================================
# 1. Home Route (Returns JSON by default)
# ======================================================

@app.get("/")
def home():
    """
    Basic GET route.
    FastAPI automatically converts dictionaries to JSON.
    """
    return {"message": "Hello, World!"}


# ======================================================
# 2. Health Check Route
# ======================================================

@app.get("/health")
def health():
    """
    Health check endpoint for monitoring systems.
    """
    return {
        "status": "OK",
        "message": "Application is healthy",
        "code": 200
    }


# ======================================================
# 3. Query Parameters (FastAPI vs Flask request.args)
# ======================================================

@app.get("/greet")
def greet(name: str = "World"):
    """
    FastAPI detects 'name' as a query parameter because it's not in the path.
    
    Example: /greet?name=Praveen
    
    Difference: No need for 'request.args.get()'. Just define it as an argument!
    """
    return {"message": f"Hello, {name}!"}


# ======================================================
# 4. Path Parameters (Dynamic URLs)
# ======================================================

@app.get("/user/{username}")
def show_user_profile(username: str):
    """
    The variable {username} in the path maps directly to the function argument.
    """
    return {"username": username, "type": str(type(username))}


# ======================================================
# 5. Path Parameters with Validation (Type Hints)
# ======================================================

@app.get("/post/{post_id}")
def show_post(post_id: int):
    """
    By hinting 'post_id: int', FastAPI ensures this route ONLY matches integers.
    If you visit /post/abc, you get a 422 Unprocessable Entity error.
    """
    return {"post_id": post_id, "type": str(type(post_id))}


# ======================================================
# 6. Combined Path & Query Parameters
# ======================================================

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None, short: bool = False):
    """
    item_id -> Path parameter
    q       -> Optional string query parameter
    short   -> Boolean query parameter (FastAPI converts 'true', '1', 'yes' to True)
    """
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is a long description for the item."})
    return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
