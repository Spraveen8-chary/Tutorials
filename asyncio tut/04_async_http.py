import asyncio
import httpx # requests
import time

"""
===========================================================================
LESSON 4: ASYNC HTTP (High-Speed API Communication)
===========================================================================

1. WHAT IS IT?
   `httpx` is a modern HTTP client for Python that supports both 
   Synchronous and Asynchronous requests.

2. WHY DO WE USE IT? (The "Library" Problem)
   The classic `requests` library is "Blocking". If you use it inside
   an async app, it will freeze the whole app while waiting for the web.
   `httpx` is "Non-Blocking" - it yields control back to the manager
   while the network is sending data.

3. INDUSTRY USE CASE (AI/ML):
   In modern AI architectures (Microservices), your server needs to talk
   to many other servers (OpenAI, VectorDB, Payment gateway).
   Using `httpx.AsyncClient`, you can send 100 requests at once without
   opening 100 different slow threads.
===========================================================================
"""

async def call_ai_api(client, name):
    print(f"[{name}] Requesting inference...")
    # 'async with' ensures the connection is opened and closed correctly
    # without blocking the main event loop.
    resp = await client.get("https://httpbin.org/get")
    print(f"[{name}] Done.")
    return f"{name}: API response received"

async def main():
    print("DEMO: Calling 5 AI APIs simultaneously.")
    start = time.perf_counter()

    # ---------------------------------------------------------
    # THE STANDARD: AsyncClient
    # Creating one client and reusing it for many tasks is very fast.
    # ---------------------------------------------------------
    async with httpx.AsyncClient() as client:
        tasks = [call_ai_api(client, f"Model_{i}") for i in range(5)]
        results = await asyncio.gather(*tasks)

    end = time.perf_counter()
    
    print("\nResults Summary:")
    for res in results: 
        print(f" - {res}")
    print(f"\nTotal time for 5 API calls: {end - start:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
