import concurrent.futures
import math
import time

def heavy_computation(workload_size):
    """Simulate CPU-intensive work like data analysis or image processing."""
    print(f"Starting computation with {workload_size:,} items...")
    
    # Simulate heavy mathematical computation
    total = 0
    for i in range(workload_size):
        # Complex calculations (pure Python, no I/O)
        value = math.sin(i) * math.cos(i) + math.sqrt(i + 1)
        total += value * math.log(i + 1)
    
    print(f"Completed computation: {workload_size:,} items")
    return {
        'workload_size': workload_size,
        'result': total,
        'computed_by': 'CPU worker'
    }

def compare_sequential_vs_multiprocess():
    """Show the power of multiprocessing for CPU work."""
    
    # Each task is a chunk of work
    work_chunks = [500_000, 500_000, 500_000, 500_000]  # 4 chunks
    
    print("=== Sequential Processing (One Brain) ===")
    start_time = time.time()
    sequential_results = []
    
    for i, chunk_size in enumerate(work_chunks, 1):
        result = heavy_computation(chunk_size)
        sequential_results.append(result)
        print(f"  Chunk {i} completed")
    
    sequential_time = time.time() - start_time
    print(f"Sequential total: {sequential_time:.2f}s\n")
    
    print("=== Multiprocess Processing (Multiple Brains) ===")
    start_time = time.time()
    multiprocess_results = []
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Submit all chunks simultaneously
        futures = [executor.submit(heavy_computation, chunk_size) 
                  for chunk_size in work_chunks]
        
        # Collect results as they complete
        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            result = future.result()
            multiprocess_results.append(result)
            print(f"  Chunk {i} completed")
    
    multiprocess_time = time.time() - start_time
    print(f"Multiprocess total: {multiprocess_time:.2f}s")
    
    speedup = sequential_time / multiprocess_time if multiprocess_time > 0 else 0
    print(f"Speedup: {speedup:.1f}x faster with multiple processes!")
    
    return sequential_results, multiprocess_results

# Run the comparison
sequential_results, process_results = compare_sequential_vs_multiprocess()
