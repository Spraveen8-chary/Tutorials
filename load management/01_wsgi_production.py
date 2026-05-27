from flask import Flask
import time

"""
===========================================================================
LESSON 1: THE WSGI SERVER (Waitress)
===========================================================================

1. THE PROBLEM:
   Flask's default 'app.run()' is a development server. It is 
   "Single-Threaded" by default. If one user is waiting for an AI result 
   that takes 10 seconds, EVERY OTHER USER is blocked. They see a 
   loading spinner until the first user is done.

2. THE SOLUTION:
   A WSGI (Web Server Gateway Interface) server like Waitress.
   It creates a "ThreadPool". This means the server can talk to many
   users at the same time using different threads.

3. INDUSTRY USE CASE:
   Small to medium-sized AI services on Windows use Waitress to handle 
   up to 50-100 simultaneous users on a single machine.
===========================================================================
"""

app = Flask(__name__)

@app.route('/')
def home():
    # This simulates a task that takes 2 seconds.
    # In 'app.run()', this would block everyone else.
    # In 'Waitress', other users can still access the site.
    time.sleep(2)
    return "Response received after 2 seconds!"

if __name__ == '__main__':
   # ---------------------------------------------------------
   # PRODUCTION CONFIGURATION
   # ---------------------------------------------------------
   # app.run(debug=True)





   from waitress import serve
   print("--- SERVER STARTING WITH WAITRESS ---")
   print("Configuration: 50 Parallel Threads")
   print("This server can now handle 50 people at the same time.")
   
   # 'threads=50' tells Waitress to hire 50 "waiters" to handle requests.
   serve(app, host='127.0.0.1', port=5000, threads=50)

"""
HOW TO TEST THE LOAD:
---------------------
1. Run this file.
2. Open 5 different browser tabs and go to http://127.0.0.1:5000.
3. Refresh all of them at once.
4. Notice how they ALL finish at almost the same time. 
   If you used app.run(), they would finish 2s, 4s, 6s... apart.
"""
