"""
========================================================
            FastAPI Request Body & Forms
========================================================

Scenario:
---------
You are building a login system. Users need to send their credentials 
either via a JSON body (for mobile apps/React) or via a standard HTML Form.

Topic:
------
1. Pydantic Models for JSON Requests
2. Form Data Handling
3. Handling Multiple HTTP Methods (GET vs POST)
4. Response Status Codes

What it is used for:
--------------------
Securely receiving and validating data sent by users in the "body" of 
an HTTP request.

Problem it solves:
------------------
Manual parsing of `request.form` or `request.json` is error-prone. 
FastAPI uses Pydantic to ensure the data is exactly what you expect 
BEFORE your function even runs.

How it is different from Flask:
-------------------------------
1. Explicit vs Implicit: Flask uses `request.form` or `request.json` 
   inside the function. FastAPI uses function arguments (`login_data: LoginSchema`).
2. Automatic Validation: In Flask, you'd check `if not username:`. 
   In FastAPI, Pydantic handles this. If a field is missing, FastAPI 
   automatically returns a 422 error.
3. Form vs JSON: In FastAPI, you use the `Form` class for form data 
   and standard models for JSON. Flask's `request` handles both, but 
   you have to know which one to look at.

Run:
----
uvicorn app:app --reload

========================================================
"""

from fastapi import FastAPI, Form, Request, HTTPException, status
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()

# ======================================================
# 1. Pydantic Model (For JSON Data)
# ======================================================

class LoginSchema(BaseModel):
    """
    Defines the structure for JSON login requests.
    FastAPI will automatically validate that incoming JSON 
    matches these fields and types.
    """
    username: str
    password: str

# ======================================================
# 2. JSON Login Route (POST)
# ======================================================

@app.post("/login-json")
def login_json(data: LoginSchema):
    """
    Handles JSON login (e.g., from an API client).
    """
    if data.username == "admin" and data.password == "secret":
        return {"message": "Login successful", "auth_type": "JSON"}
    else:
        if data.username == "praveen" and data.password == "12345":
            return {"message": "Login Successful as a Praveen", "auth_type": "JSON"}
        
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )

# ======================================================
# 3. Form Login Route (POST)
# ======================================================

@app.post("/login-form")
def login_form(username: str = Form(...), password: str = Form(...)):
    """
    Handles standard HTML Form submissions.
    'Form(...)' tells FastAPI to look for these fields in the Form body.
    """
    if username == "admin" and password == "secret":
        return {"message": "Login successful", "auth_type": "FORM"}
    
    return {"message": "Invalid credentials"}

# ======================================================
# 4. Display Login Form (GET)
# ======================================================

@app.get("/login", response_class=HTMLResponse)
def show_login_page():
    """
    Returns a simple HTML form to test the /login-form route.
    """
    return """
    <html>
        <body>
            <h2>Login Form (FastAPI)</h2>
            <form action="/login-form" method="post">
                Username: <input type="text" name="username"><br>
                Password: <input type="password" name="password"><br>
                <button type="submit">Login</button>
            </form>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
