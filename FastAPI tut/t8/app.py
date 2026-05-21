"""
========================================================
                FastAPI Streaming
========================================================

Scenario:
---------
You are building an AI Chatbot (like ChatGPT). The AI takes 10 seconds 
to think of a long answer. You want to show the words to the user 
one-by-one as they are generated, rather than making them wait 10 seconds.

Topic:
------
1. `StreamingResponse`
2. Python Generators (`yield`)
3. Efficient memory usage for large files

What it is used for:
--------------------
Streaming AI responses (tokens), serving large video/audio files, 
or sending massive amounts of data without crashing the server's RAM.

Problem it solves:
------------------
If you try to return a 1GB file normally, the server must load the 
entire 1GB into its RAM first. Streaming sends it in "chunks" (e.g., 1MB at a time).

How it is different from Flask:
-------------------------------
1. Async Generators: FastAPI fully supports `async for` and async generators 
   for streaming, making it much more efficient for I/O bound tasks.
2. Built-in Class: You use `from fastapi.responses import StreamingResponse`. 
   In Flask, you return a `Response` object with a generator.
3. Performance: FastAPI's underlying server (uvicorn) is optimized for 
   keeping many streaming connections open at once.

Run:
----
uvicorn app:app --reload

========================================================
"""

import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

# ======================================================
# 1. ASYNC GENERATOR
# ======================================================

async def ai_response_generator():
    """
    Simulates an AI generating a response word-by-word.
    Using 'async' allows the server to handle other users 
    while this one is 'thinking'.
    """
    text = ("FastAPI streaming is powerful! It allows you to send data "
            "chunk-by-chunk. This is how modern AI apps provide a "
            "snappy user experience.")
    
    for word in text.split():
        yield word + " "
        await asyncio.sleep(0.3) # Simulate "thinking" time

# ======================================================
# 2. STREAMING ROUTE
# ======================================================

@app.get("/stream-ai")
async def stream_ai():
    """
    Returns the AI response as a stream.
    The browser will receive each word as it is yielded.
    """
    return StreamingResponse(ai_response_generator(), media_type="text/plain")

# ======================================================
# 3. LARGE DATA SIMULATION
# ======================================================

def large_data_generator():
    """
    A standard generator for non-async streaming (e.g., large CSV exports).
    """
    for i in range(100):
        yield f"Row {i}, Data Point A, Data Point B\n"

@app.get("/download-csv")
def download_csv():
    return StreamingResponse(
        large_data_generator(), 
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=export.csv"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
