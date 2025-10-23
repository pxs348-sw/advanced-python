import concurrent.futures
import math
import time

def small_task_demonstration():
    """Show when multiprocessing overhead isn't worth it."""
    
    def tiny_computation(n):
        """Very small computation - overhead will dominate."""
        return sum(range(n))
    
    small_tasks = [1000] * 10  # 10 tiny tasks
    
    print("=== Small Tasks: Sequential vs Multiprocess ===")
    
    # Sequential
    start = time.time()
    seq_results = [tiny_computation(n) for n in small_tasks]
    seq_time = time.time() - start
    print(f"Sequential: {seq_time:.4f}s")
    
    # Multiprocess (will be slower due to overhead!)
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        proc_results = list(executor.map(tiny_computation, small_tasks))
    proc_time = time.time() - start
    print(f"Multiprocess: {proc_time:.4f}s")
    
    print(f"Overhead cost: {proc_time/seq_time:.1f}x slower!")
    print("Lesson: Use multiprocessing for substantial work, not tiny tasks")

small_task_demonstration()


