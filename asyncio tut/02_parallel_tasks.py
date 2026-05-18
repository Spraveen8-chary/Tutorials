import asyncio
import time

"""
===========================================================================
LESSON 2: GATHER (Concurrency & Parallelism)
===========================================================================

1. WHAT IS IT?
   `asyncio.gather()` is a tool that takes a list of tasks and starts them
   all at the EXACT same time. It then waits for all of them to finish.

2. WHY DO WE USE IT? (The "Chain" Problem)
   If you have 3 tasks that each take 1 second:
   - Synchronous: 1s + 1s + 1s = 3 seconds total.
   - Async Gather: Starts all 3 at 0.0s -> All finish at 1.0s = 1 second total.
   It reduces "Latency" (waiting time for the user).

3. INDUSTRY USE CASE (AI/ML):
   Imagine an AI "Search Agent". It needs to:
   - Search Google.
   - Search Wikipedia.
   - Search a Vector Database.
   Instead of searching one-by-one, it 'gathers' all results simultaneously.
===========================================================================
"""

async def search_google():
    print("[Search] Starting Google search...")
    await asyncio.sleep(1.5)
    return "Google: Found 10 Flask tutorials."

async def search_wiki():
    print("[Wiki] Starting Wikipedia lookup...")
    await asyncio.sleep(1.0)
    return "Wiki: Flask is a micro-web framework."

async def search_database():
    print("[DB] Querying Vector Database...")
    await asyncio.sleep(0.5)
    return "DB: Local context found in lesson 2."

async def main():
    print("DEMO: Running 3 search tasks in parallel.")
    start = time.perf_counter()

    # ---------------------------------------------------------
    # THE POWER: asyncio.gather
    # We pass the function calls as arguments.
    # ---------------------------------------------------------
    results = await asyncio.gather(
        search_google(),
        search_wiki(),
        search_database()
    )

    end = time.perf_counter()
    
    print("\nCombined Results:")
    for r in results: print(f" - {r}")
    
    # Notice: Total time is ~1.5s (the slowest task), not 3.0s!
    print(f"\nTotal Latency: {end - start:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
