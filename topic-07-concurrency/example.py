import threading
import time
import multiprocessing
import requests

def demonstrate_io_vs_cpu_work():
    """Show why threads help I/O but not CPU work."""
    
    def io_task(task_id, duration):
        """Simulate I/O work - waiting for something"""
        print(f"I/O Task {task_id} starting (will wait {duration}s)")
        time.sleep(duration)  # This releases the GIL!
        print(f"I/O Task {task_id} completed")
        return f"IO-{task_id}"
    
    def cpu_task(task_id, work_amount):
        """Simulate CPU work - actual computation"""
        print(f"CPU Task {task_id} starting (will compute {work_amount} items)")
        # This DOESN'T release the GIL - pure Python computation
        result = sum(i ** 2 for i in range(work_amount))
        print(f"CPU Task {task_id} completed")
        return result
    
    print("=== I/O Work: Sequential vs Threaded ===")
    
    # Sequential I/O (slow)
    start = time.time()
    io_task(1, 1)
    io_task(2, 1) 
    sequential_io_time = time.time() - start
    print(f"Sequential I/O time: {sequential_io_time:.2f}s\n")
    
    # Threaded I/O (fast!)
    start = time.time()
    threads = [
        threading.Thread(target=io_task, args=(1, 1)),
        threading.Thread(target=io_task, args=(2, 1))
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    threaded_io_time = time.time() - start
    print(f"Threaded I/O time: {threaded_io_time:.2f}s")
    print(f"I/O speedup: {sequential_io_time / threaded_io_time:.1f}x\n")
    print("=== CPU Work: Sequential vs Threaded ===")
    
    # Sequential CPU
    start = time.time()
    cpu_task(1, 1000000)
    cpu_task(2, 1000000)
    sequential_cpu_time = time.time() - start
    print(f"Sequential CPU time: {sequential_cpu_time:.2f}s\n")
    
    # Threaded CPU (won't help much due to GIL)
    start = time.time()
    threads = [
        threading.Thread(target=cpu_task, args=(1, 1000000)),
        threading.Thread(target=cpu_task, args=(2, 1000000))
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    threaded_cpu_time = time.time() - start
    print(f"Threaded CPU time: {threaded_cpu_time:.2f}s")
    print(f"CPU 'speedup': {sequential_cpu_time / threaded_cpu_time:.1f}x (should be ~1.0)")

# Run the demonstration
demonstrate_io_vs_cpu_work()

