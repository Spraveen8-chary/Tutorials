"""
========================================================
                FastAPI URL Building
========================================================

Scenario:
---------
You want to generate URLs for your routes dynamically without hardcoding them. 
This is useful if you decide to change your URL structure later.

Topic:
------
Generating URLs using the Request object's `url_for` method.

What it is used for:
--------------------
Creating links to other parts of your API or website within your code.

Problem it solves:
------------------
Prevents "Broken Links" within your app if you rename a path. Instead of 
updating every link to `/login`, you just refer to the function name `login`.

How it is different from Flask:
-------------------------------
1. Request Object: In Flask, `url_for` is a global function. In FastAPI, 
   you must include `request: Request` in your function arguments to access 
   `request.url_for()`.
2. Async Ready: FastAPI is built for async, and the way it handles context 
   is more explicit than Flask's thread-local globals.

Run:
----
uvicorn app:app --reload

========================================================
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", name="index")
def index():
    return {"message": "Welcome to the index"}

@app.get("/login", name="login_route")
def login():
    return {"message": "Please login"}

@app.get("/user/{username}", name="profile")
def profile(username: str):
    return {"user": username}

@app.get("/test-urls")
def test_urls(request: Request):
    """
    Demonstrates how to generate URLs for other routes.
    
    NOTE: Unlike Flask's url_for, FastAPI's url_for returns a URL object 
    that you might need to cast to string.
    """
    index_url = request.url_for("index")
    login_url = request.url_for("login_route")
    profile_url = request.url_for("profile", username="Praveen")
    
    # You can also add query parameters manually to the generated URL
    login_with_next = f"{login_url}?next=/"

    return {
        "index": str(index_url),
        "login": str(login_url),
        "login_with_next": login_with_next,
        "profile": str(profile_url)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)




"""
URL_FOR examples scenario

if user_details:
    return redirect(url_for(login))
else:
    return url_for(login_page)

"""