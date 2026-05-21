"""
========================================================
            FastAPI Security & Dependencies
========================================================

Scenario:
---------
You have an expensive AI API. You only want people with a valid 
"API Key" to use it. Additionally, you want to limit how many times 
per minute they can call it (Rate Limiting).

Topic:
------
1. Dependency Injection (`Depends`)
2. API Key Authentication
3. Reusable Security logic

What it is used for:
--------------------
Protecting your routes from unauthorized access and ensuring your 
server isn't overloaded by too many requests.

Problem it solves:
------------------
Instead of writing `if key != "secret":` inside EVERY function, 
you create a "Dependency" that FastAPI runs automatically before 
your function starts.

How it is different from Flask:
-------------------------------
1. Decorators vs Dependencies: Flask uses decorators (`@require_api_key`). 
   FastAPI uses `Depends()`. Dependencies are more powerful because 
   they can be nested and shared across different routes easily.
2. Built-in Security: FastAPI has a `fastapi.security` module with 
   helpers for OAuth2, JWT, and API Keys. Flask requires 
   `Flask-Login` or `Flask-Security`.
3. Auto-Docs: Security dependencies automatically add "Authorize" 
   buttons to your Swagger (/docs) page!

Run:
----
uvicorn app:app --reload

========================================================
"""

from fastapi import FastAPI, Depends, HTTPException, Header, status

app = FastAPI()

# ======================================================
# 1. THE SECURITY DEPENDENCY
# ======================================================

VALID_API_KEYS = ["sk-fastapi-12345", "sk-ml-99999"]

async def verify_api_key(x_api_key: str = Header(...)):
    """
    A dependency that looks for 'X-API-Key' in the request headers.
    If not found or invalid, it stops the request.
    """
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or Missing API Key"
        )
    return x_api_key

# ======================================================
# 2. PROTECTED ROUTES
# ======================================================

@app.get("/")
def public_home():
    return {"message": "This is a public page."}

@app.get("/api/secret-data")
def get_secret_data(api_key: str = Depends(verify_api_key)):
    """
    By adding 'Depends(verify_api_key)', this route is now LOCKED.
    FastAPI will first run 'verify_api_key'. If it fails, 
    this code never runs.
    """
    return {
        "message": "You have accessed the secret data!",
        "used_key": api_key,
        "data": [1, 2, 3, 4, 5]
    }

# ======================================================
# 3. GLOBAL DEPENDENCY (Locking everything)
# ======================================================

# If you wanted to lock the ENTIRE API, you would do:
# app = FastAPI(dependencies=[Depends(verify_api_key)])

@app.get("/rate-limit-info")
def rate_limit():
    return {
        "info": "For rate limiting, FastAPI users often use 'slowapi' "
                "(a port of Flask-Limiter) or specialized Middleware."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
