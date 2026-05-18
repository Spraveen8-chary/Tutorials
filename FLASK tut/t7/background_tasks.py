"""
* Celery is a Python tool used to run background tasks asynchronously.
* It is commonly used with Flask applications.
* Celery helps Flask avoid blocking while performing heavy operations.
* Tasks like email sending, AI prediction, file upload, and PDF generation can run in the background.
* Flask sends tasks to Celery using a message broker like Redis or RabbitMQ.
* Celery workers pick tasks from the queue and execute them separately.
* This improves application speed and user experience.
* Celery supports retries if a task fails due to network/API issues.
* It also supports scheduled tasks using Celery Beat.
* Celery is mainly used to improve scalability, performance, and handling of long-running tasks.


ASYNCHRONOUS TASKS FOR AI/ML (t7)
================================

WHY USE CELERY?
---------------
In AI/ML, running a model (inference or training) often takes 10+ seconds.
If you run this inside a standard Flask route:
1. The user's browser waits until the task is done.
2. The browser might "Time Out" and show an error.
3. The server can't handle other users while it's busy with the model.

CELERY solves this by moving the task to a "Background Worker."

ARCHITECTURE:
-------------
[Client (Browser)]  <-- (Polls for Status) --> [Flask App]
        |                                         |
        | (1. Request Task)                       | (2. Queue Task)
        v                                         v
   [Flask Route] ---------------------------> [Redis (Broker)]
                                                  |
                                                  | (3. Pick up Task)
                                                  v
                                           [Celery Worker]
                                           (Runs ML Model)

HOW TO RUN THIS TUTORIAL:
-------------------------
1. Install Redis on your machine (or use a Docker container).
2. Start the Redis server.
3. Open two terminal windows:
   - Terminal 1 (The Worker):
     cd t7
     celery -A app.celery worker --loglevel=info
   - Terminal 2 (The Flask App):
     python t7/app.py

Note: On Windows, Celery might need 'eventlet' or 'solo' to work properly:
pip install eventlet
celery -A app.celery worker --loglevel=info -P eventlet



celery = [t1, t2, t3, t4, t5, t6, t7]
t1 = "Flask is a Python web framework for building web applications."
t2 = "Celery is a tool for running background tasks asynchronously."

all tasks will run asynhronously, allowing the Flask app to remain responsive while 
heavy AI/ML tasks are processed in the background.
"""

def get_summary():
    return "Celery + Redis allow for long-running AI tasks without blocking the UI."
