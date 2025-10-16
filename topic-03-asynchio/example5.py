import asyncio
import aiohttp
import time

async def fetch_url(session, url, delay=1):
    """Simulate fetching data from a URL."""
    print(f"Starting fetch: {url}")
    await asyncio.sleep(delay)  # Simulate network delay
    print(f"Finished fetch: {url}")
    return f"Data from {url}"

async def gather_example():
    """Using gather() to run multiple operations concurrently."""
    urls = [
        "https://api.example1.com/data",
        "https://api.example2.com/data", 
        "https://api.example3.com/data"
    ]
    
    start_time = time.time()
    
    # Method 1: Using gather - starts all at once, waits for all
    print("=== Using asyncio.gather() ===")
    tasks = [fetch_url(None, url, delay=2) for url in urls]
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"Gathered {len(results)} results in {end_time - start_time:.2f}s")
    print(f"Results: {results}")
    return results


# GATHER WITH EXCEPTIONS

async def gather_with_exceptions():
    """Handle exceptions in concurrent operations."""
    
    async def might_fail(name, should_fail=False):
        await asyncio.sleep(1)
        if should_fail:
            raise ValueError(f"Task {name} failed!")
        print(f"Task {name} succeeded")
        return f"Success: {name}"
    
    print("\n=== Exception Handling with gather() ===")
    
    tasks = [
        might_fail("Task1", False),
        might_fail("Task2", True),   # This will fail
        might_fail("Task3", False)
    ]
    
    # Default behavior: stops on first exception
    try:
        print("Trying gather() without return_exceptions...")
        results = await asyncio.gather(*tasks)
        print(f"All succeeded: {results}")
    except ValueError as e:
        print(f"gather() failed fast: {e}")
    
    # Better behavior: collect all results including exceptions
    print("\nTrying gather() with return_exceptions=True...")
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i+1} failed: {result}")
        else:
            print(f"Task {i+1} succeeded: {result}")

# asyncio.run(gather_with_exceptions())

# AS_COMPLETED example

# import asyncio
import random

async def download_file(file_id, size_mb):
    """Simulate downloading a file of given size."""
    # Simulate variable download time based on size + some randomness
    download_time = size_mb * 0.1 + random.uniform(0.5, 2.0)
    
    print(f"Starting download of file {file_id} ({size_mb}MB)")
    await asyncio.sleep(download_time)
    print(f"✓ Completed download of file {file_id} in {download_time:.1f}s")
    
    return {"file_id": file_id, "size_mb": size_mb, "time": download_time}

async def download_with_progress():
    """Download files and show progress as they complete."""
    files = [
        (1, 10), (2, 5), (3, 15), (4, 8), (5, 12)
    ]
    
    print("=== Download Progress with as_completed() ===")
    
    # Create all download tasks
    tasks = [download_file(file_id, size) for file_id, size in files]
    
    completed_count = 0
    total_size = 0
    
    # Process results as they complete (not in order!)
    for coro in asyncio.as_completed(tasks):
        result = await coro
        completed_count += 1
        total_size += result["size_mb"]
        
        print(f"📊 Progress: {completed_count}/{len(files)} files completed")
        print(f"📁 Total downloaded: {total_size}MB")
        print(f"⚡ Last completed: File {result['file_id']} ({result['size_mb']}MB)")
        print("-" * 50)

async def compare_gather_vs_as_completed():
    """Compare gather() vs as_completed() approaches."""
    
    files = [(1, 3), (2, 1), (3, 2)]  # Different sizes = different completion times
    
    print("\n=== Comparison: gather() vs as_completed() ===")
    
    # Using gather() - wait for all, then process all
    print("Using gather() - batch processing:")
    start_time = asyncio.get_event_loop().time()
    tasks = [download_file(f"G{file_id}", size) for file_id, size in files]
    results = await asyncio.gather(*tasks)
    
    print("Processing all results at once:")
    for result in results:
        print(f"  Processed file {result['file_id']}")
    
    # Using as_completed() - process each as it finishes
    print("\nUsing as_completed() - streaming processing:")
    tasks = [download_file(f"S{file_id}", size) for file_id, size in files]
    
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"  Immediately processed file {result['file_id']}")

# asyncio.run(download_with_progress())
# asyncio.run(compare_gather_vs_as_completed())
