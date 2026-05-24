"""
========================================================
            FastAPI Templates & Static Files
========================================================

Scenario:
---------
You want to build a full-stack website where the server renders HTML 
pages and serves CSS/JavaScript files.

Topic:
------
1. Jinja2 Templates integration
2. Serving Static Files (CSS, Images, JS)
3. Directory Structure

What it is used for:
--------------------
Building traditional web applications where HTML is generated on the server.

Problem it solves:
------------------
Allows you to separate logic (Python) from presentation (HTML/CSS), 
and makes your site look good by serving stylesheets and scripts.

How it is different from Flask:
-------------------------------
1. Explicit Setup: Flask looks for 'templates/' and 'static/' folders 
   automatically. FastAPI requires you to "Mount" the static files 
   and initialize the `Jinja2Templates` object.
2. Async Rendering: While Jinja2 is synchronous, FastAPI's structure 
   makes it clear how to pass the `request` object to the template, 
   which is mandatory in FastAPI.

Run:
----
uvicorn app:app --reload

========================================================
"""

import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# 1. SETUP STATIC FILES
# We 'mount' a directory to a path.
# This means files in the local 'static' folder will be available at /static
# (Create the 'static/css' folder and a 'style.css' file first!)

app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. SETUP TEMPLATES
# We tell FastAPI where to look for HTML files.

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_item(request: Request, username: str = "Developer"):
    """
    Renders the index.html template.
    IMPORTANT: You MUST pass the 'request' in the context dictionary.
    """
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "username": username}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
