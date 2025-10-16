import asyncio
import time

async def fetch_data(source, delay):
    """Simulate fetching data with a delay."""
    print(f"Starting fetch from {source}")
    await asyncio.sleep(delay)  # Simulate I/O delay
    print(f"Finished fetching from {source}")
    return f"Data from {source}"

async def sequential_execution():
    """Run tasks one after another - SLOW."""
    print("=== Sequential Async Execution ===")
    start_time = time.time()
    
    # Wait for each one to finish before starting the next
    result1 = await fetch_data("API-1", 2)
    result2 = await fetch_data("API-2", 1)
    result3 = await fetch_data("API-3", 1.5)
    
    total_time = time.time() - start_time
    print(f"Sequential total time: {total_time:.2f}s")
    return [result1, result2, result3]

async def concurrent_execution():
    """Run tasks concurrently - FAST."""
    print("\n=== Concurrent Async Execution ===")
    start_time = time.time()
    
    # Start all tasks at once
    task1 = asyncio.create_task(fetch_data("API-1", 2))
    task2 = asyncio.create_task(fetch_data("API-2", 1))
    task3 = asyncio.create_task(fetch_data("API-3", 1.5))
    
    # Wait for all to complete
    result1 = await task1
    result2 = await task2
    result3 = await task3
    
    total_time = time.time() - start_time
    print(f"Concurrent total time: {total_time:.2f}s")
    return [result1, result2, result3]

# Compare both approaches
async def compare_execution():
    await sequential_execution()
    await concurrent_execution()

asyncio.run(compare_execution())