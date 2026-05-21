"""
========================================================
                FastAPI File Uploads
========================================================

Scenario:
---------
You are building a profile page where users can upload their 
profile pictures or submit PDF documents.

Topic:
------
1. `UploadFile` vs `File`
2. Handling file metadata (filename, content_type)
3. Storing files on the server safely

What it is used for:
--------------------
Accepting images, documents, or any other file type from a user.

Problem it solves:
------------------
Manually handling raw byte streams from forms is difficult. 
`UploadFile` provides a clean interface to read the file, 
get its name, and save it.

How it is different from Flask:
-------------------------------
1. Spooling to Disk: `UploadFile` in FastAPI uses a "Spooling" 
   system. Files up to a certain size are kept in RAM; larger 
   files are stored in a temporary file on disk. This prevents 
   RAM crashes. Flask's `request.files` does something similar 
   but is less explicit.
2. Metadata: `UploadFile` gives you easy access to `filename`, 
   `content_type`, and `file` (the file-like object) directly 
   in the function arguments.
3. Async Support: You can use `await file.read()` which allows 
   FastAPI to handle other requests while the file is being 
   uploaded.

Run:
----
uvicorn app:app --reload

========================================================
"""

import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ======================================================
# 1. FILE UPLOAD ROUTE
# ======================================================

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    'UploadFile' is preferred over 'File(bytes)' because:
    - It stores metadata (filename).
    - It's memory efficient (doesn't load everything into RAM).
    """
    # 1. Validate File Extension (Security)
    allowed_extensions = ["jpg", "png", "pdf"]
    file_ext = file.filename.split(".")[-1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type.")

    # 2. Save the file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # We use 'shutil' to copy the file stream to our folder
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "File uploaded successfully!"
    }

# ======================================================
# 2. MULTIPLE FILE UPLOADS
# ======================================================

from typing import List

@app.post("/upload-multiple")
async def upload_multiple(files: List[UploadFile] = File(...)):
    filenames = []
    for file in files:
        filenames.append(file.filename)
        # (Save logic would go here)
    return {"uploaded_files": filenames}

# ======================================================
# 3. TEST HTML PAGE
# ======================================================

@app.get("/", response_class=HTMLResponse)
def main():
    return """
    <body>
        <h2>Single File Upload</h2>
        <form action="/upload" enctype="multipart/form-data" method="post">
            <input name="file" type="file">
            <input type="submit">
        </form>
        
        <h2>Multiple File Upload</h2>
        <form action="/upload-multiple" enctype="multipart/form-data" method="post">
            <input name="files" type="file" multiple>
            <input type="submit">
        </form>
    </body>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
