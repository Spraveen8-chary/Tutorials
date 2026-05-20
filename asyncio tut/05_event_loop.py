import asyncio
import time

"""
===========================================================================
LESSON 5: THE EVENT LOOP (The "Brain" of Asyncio)
===========================================================================

1. WHAT IS IT?
   The Event Loop is a continuous loop that:
   - Monitors all running tasks (coroutines).
   - When a task hits an 'await', the loop pauses it and looks for another 
     task that is ready to run.
   - It is the "Manager" that handles all the context switching.

2. WHY IS IT IMPORTANT?
   Python usually runs one line at a time. The Event Loop allows us to
   simulate "Doing many things at once" using only ONE thread. 
   This is much lighter and faster than creating 1000 separate threads.

3. HOW IT WORKS (The Analogy):
   Think of a waiter in a restaurant:
   - Waiter takes Order A (Task A).
   - Waiter gives Order A to the kitchen (Kitchen = The Network/Database).
   - THE WAITER DOES NOT STAND IN THE KITCHEN WAITING! (That would be Blocking).
   - The Waiter goes to Table B to take another order (Context Switch).
   - When the kitchen rings the bell, the Waiter goes back to Table A.

4. INDUSTRY USE CASE (AI/ML):
   In a high-traffic AI API, the Event Loop is what allows the server to 
   handle 5000 incoming user messages. It spends 99% of its time 
   "switching" between users who are waiting for their AI responses.
===========================================================================
"""

async def task_worker(name, work_duration):
    """A worker that simulates a task that involves some waiting."""
    print(f"  [Loop] Task {name}: Starting. I will 'wait' for {work_duration}s.")
    
    # This 'await' tells the Event Loop: "I am going to be busy waiting. 
    # Please go check if any other task needs your attention!"
    await asyncio.sleep(work_duration)
    
    print(f"  [Loop] Task {name}: Finished after {work_duration}s.")
    return f"Result {name}"

async def main():
    print("--- DEMO: THE EVENT LOOP IN ACTION ---")
    # print("Notice how Task B starts even though Task A isn't finished!\n")
    
    # We create two tasks with different durations.
    # Task A takes 3 seconds, Task B takes 1 second.
    
    # ---------------------------------------------------------
    # WATCH THE OUTPUT CAREFULLY:
    # 1. Task A starts.
    # 2. Task A 'awaits' (pauses).
    # 3. The Loop immediately jumps to Task B.
    # 4. Task B starts.
    # 5. Task B finishes (because it's shorter).
    # 6. Task A finally finishes.
    # ---------------------------------------------------------
    
    await asyncio.gather(
        task_worker("A", 13),
        task_worker("B", 10)
    )

    print("\n--- DEMO FINISHED ---")

if __name__ == "__main__":
    # asyncio.run() creates the Event Loop and runs the main() coroutine inside it.
    asyncio.run(main())

"""
SUMMARY OF THE LOOP CYCLE:
--------------------------
Step 1: Loop starts main().
Step 2: Loop sees Task A and starts it.
Step 3: Task A says 'await'. Loop marks Task A as "Waiting".
Step 4: Loop looks for other work -> Sees Task B and starts it.
Step 5: Task B says 'await'. Loop marks Task B as "Waiting".
Step 6: Loop keeps spinning. It sees Task B's timer is up! It wakes up Task B.
Step 7: Task B finishes.
Step 8: Loop sees Task A's timer is up! It wakes up Task A.
Step 9: Task A finishes.
"""
