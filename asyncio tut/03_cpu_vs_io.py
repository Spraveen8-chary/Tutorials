import asyncio
import time
from concurrent.futures import ProcessPoolExecutor

"""
===========================================================================
LESSON 3: EXECUTORS (Handling Heavy Math / CPU Tasks)
===========================================================================

1. WHAT IS IT?
   An 'Executor' is a separate pool of Workers (threads or processes).
   `run_in_executor` allows you to offload heavy work to these workers.

2. WHY DO WE USE IT? (The "Freezing" Problem)
   Asyncio is built for WAITING (Network/Disk). It is NOT built for 
   heavy calculation. If you try to run a heavy AI model inference
   directly inside an async function, the whole Event Loop freezes. 
   No other code can run. No other users can connect.

3. INDUSTRY USE CASE (AI/ML):
   In Production, you use `run_in_executor` to call `model.predict()`.
   The math happens in a background process, while the main Event Loop 
   remains free to talk to other users and handle the UI.
===========================================================================
"""

def heavy_matrix_math():
    """
    This is a standard Python function (Synchronous).
    It simulates 3 seconds of heavy CPU-intensive ML calculation.
    """
    print("[CPU Worker] Starting heavy math...")
    start = time.time()
    # Busy-loop keeps the CPU 100% occupied
    while time.time() - start < 3:
        pass 
    print("[CPU Worker] Calculation finished.")
    return "AI Result: 0.99"

async def main():
    loop = asyncio.get_running_loop()
    print("DEMO: Running heavy math without freezing the server.")
    start_time = time.perf_counter()

    # ---------------------------------------------------------
    # THE TRICK: Moving CPU work to a separate Process
    # This keeps the main thread free to handle other requests.
    # ---------------------------------------------------------
    with ProcessPoolExecutor() as pool:
        # We start the CPU task in the background pool
        # loop.run_in_executor(pool, function_name)
        result = await loop.run_in_executor(pool, heavy_matrix_math)

    end_time = time.perf_counter()
    print(f"Final Result: {result}")
    print(f"Total time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
