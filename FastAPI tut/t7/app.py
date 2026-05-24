"""
========================================================
            FastAPI Background Tasks
========================================================

Scenario:
---------
A user signs up, and you need to send them a welcome email. Sending 
an email takes 2-3 seconds. You don't want the user to wait for that 
to finish before seeing a "Success" page.

Topic: 
------
1. Built-in `BackgroundTasks`
2. Difference between Background Tasks and Async functions
3. Comparison with Celery

What it is used for:
--------------------
Tasks that can happen after a response is sent: sending emails, 
generating report files, or cleaning up logs.

Problem it solves:
------------------
Prevents the user's browser from "spinning" or timing out while the 
server performs a slow, non-critical operation.

How it is different from Flask:
-------------------------------
1. Built-in: FastAPI has a `BackgroundTasks` class built-in. Flask 
   requires Celery, Redis, or other complex tools even for simple tasks.
2. Lightweight: FastAPI's background tasks run in the same process 
   as your app (using the event loop), making them very easy to setup.
3. Type Hinting: Just add `background_tasks: BackgroundTasks` to 
   your function signature!

Run:
----
uvicorn app:app --reload

========================================================
"""

from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()

# ======================================================
# 1. THE HEAVY FUNCTION
# ======================================================

def send_email_notification(email: str, message: str):
    """
    A function that simulates a slow operation (like sending an email).
    """
    print(f"--- STARTING: Sending email to {email} ---")
    time.sleep(5) # Simulates network delay
    print(f"--- FINISHED: Email sent with message: {message} ---")

# ======================================================
# 2. THE API ROUTE
# ======================================================

@app.post("/signup")
async def signup(email: str, background_tasks: BackgroundTasks):
    """
    1. User submits their email.
    2. We schedule the 'send_email' function to run in the background.
    3. We return the response IMMEDIATELY.
    """
    # Schedule the task
    # (Function to run, Arguments for that function)
    background_tasks.add_task(send_email_notification, email, "Welcome to FastAPI!")
    
    return {
        "message": "Signup successful! Your welcome email is being sent in the background.",
        "note": "Notice how this response was instant, even though the 'email' takes 5 seconds."
    }

# ======================================================
# 3. COMPLEX TASKS (Celery Hint)
# ======================================================

@app.get("/celery-info")
def celery_info():
    return {
        "built_in": "Great for simple tasks (emails, small logs).",
        "celery": "Necessary for HEAVY tasks (AI models, Video processing) "
                  "that need to run on separate servers."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
