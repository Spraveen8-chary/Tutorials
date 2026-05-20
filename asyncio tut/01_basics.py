import asyncio
import time

"""
===========================================================
UNDERSTANDING NORMAL vs ASYNC EXECUTION
===========================================================

We will compare:

1. Normal Sequential Execution
2. Async Sequential Execution
3. Async Concurrent Execution

This will clearly show WHY asyncio is powerful.
===========================================================
"""


# =========================================================
# NORMAL FUNCTION (BLOCKING)
# =========================================================

def normal_task(name):
    print(f"[NORMAL START] {name}")

    # BLOCKS the entire program
    time.sleep(2)

    print(f"[NORMAL END] {name}")

    return f"Result of {name}"


# =========================================================
# ASYNC FUNCTION (NON-BLOCKING)
# =========================================================

async def async_task(name):
    print(f"[ASYNC START] {name}")

    # DOES NOT block the event loop
    await asyncio.sleep(2)

    print(f"[ASYNC END] {name}")

    return f"Result of {name}"


# =========================================================
# 1. NORMAL SEQUENTIAL EXECUTION
# =========================================================

def run_normal():
    print("\n================ NORMAL EXECUTION ================")

    start = time.perf_counter()

    res1 = normal_task("Alice")
    res2 = normal_task("Bob")

    end = time.perf_counter()

    print(f"\nResults: {res1}, {res2}")
    print(f"Total Time: {end - start:.2f} seconds")


# =========================================================
# 2. ASYNC BUT STILL SEQUENTIAL
# =========================================================

async def run_async_sequential():
    print("\n============ ASYNC SEQUENTIAL EXECUTION ============")

    start = time.perf_counter()

    # STILL SEQUENTIAL
    res1 = await async_task("Alice")
    res2 = await async_task("Bob")

    end = time.perf_counter()

    print(f"\nResults: {res1}, {res2}")
    print(f"Total Time: {end - start:.2f} seconds")


# =========================================================
# 3. REAL ASYNC CONCURRENT EXECUTION
# =========================================================

async def run_async_concurrent():
    print("\n============ ASYNC CONCURRENT EXECUTION ============")

    start = time.perf_counter()

    # Create tasks
    task1 = asyncio.create_task(async_task("Alice"))
    task2 = asyncio.create_task(async_task("Bob"))

    # Run BOTH together
    results = await asyncio.gather(task1, task2)

    end = time.perf_counter()

    print(f"\nResults: {results}")
    print(f"Total Time: {end - start:.2f} seconds")


# =========================================================
# MAIN
# =========================================================

async def main():

    # Normal Blocking
    run_normal()

    # Async but sequential
    await run_async_sequential()

    # Real concurrent async
    await run_async_concurrent()


# =========================================================
# START EVENT LOOP
# =========================================================

if __name__ == "__main__":
    asyncio.run(main())