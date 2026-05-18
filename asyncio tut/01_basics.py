import asyncio
import time

"""
===========================================================================
LESSON 1: ASYNC & AWAIT (The Foundation)
===========================================================================

1. WHAT IS IT?
   'async' defines a coroutine (a function that can be paused).
   'await' is the pause button. It tells Python: "Stop here, let the server
   do other things, and come back when this specific task is finished."

2. WHY DO WE USE IT?
   In standard Python, code is "Synchronous" (one line at a time).
   If you have a task that takes 5 seconds (like an API call), the WHOLE
   program freezes. In a web app, this means no other user can use the app.
   Async/Await solves this by allowing "Non-Blocking" execution.

3. INDUSTRY USE CASE (AI/ML):
   Think of a Chatbot like ChatGPT. While the AI is "thinking" or the 
   network is "waiting" for the next token from OpenAI, the server 
   shouldn't freeze. It should be able to accept messages from 500 other 
   users at the same time. Asyncio makes this possible on a single thread.
===========================================================================
"""

async def simulate_api_call(user_id):
    """
    Simulates calling an AI model API which takes 2 seconds.
    """
    print(f"--- [TASK START] Requesting AI response for User {user_id} ---")
    
    # ---------------------------------------------------------
    # THE MAGIC: asyncio.sleep vs time.sleep
    # time.sleep(2) would FREEZE the whole computer.
    # asyncio.sleep(2) tells the manager "I'm waiting, go do other work!"
    # ---------------------------------------------------------
    await asyncio.sleep(2) 
    
    print(f"--- [TASK END] AI response ready for User {user_id} ---")
    return f"Response for {user_id}"

async def main():
    print("DEMO: Handling tasks one-by-one but without freezing.")
    start = time.perf_counter()

    # We await the first task
    res1 = await simulate_api_call("Alice")
    # We await the second task
    res2 = await simulate_api_call("Bob")

    end = time.perf_counter()
    print(f"\nFinal Results: {res1}, {res2}")
    print(f"Total Time: {end - start:.2f} seconds")

if __name__ == "__main__":
    # Start the 'Event Loop' (The Manager)
    asyncio.run(main())
