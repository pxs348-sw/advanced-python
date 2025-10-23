import queue
import threading
import time
import random

def simple_producer_consumer():
    """Demonstrate basic producer-consumer pattern."""
    
    # The "conveyor belt" between producer and consumer
    work_queue = queue.Queue(maxsize=5)  # Limit queue size to prevent overload
    
    def producer(name, items_to_produce):
        """Produces work items (like taking orders)."""
        print(f"Producer {name} starting...")
        
        for i in range(items_to_produce):
            # Create work item
            work_item = f"{name}-item-{i+1}"
            
            # Put it on the queue (will block if queue is full)
            work_queue.put(work_item)
            print(f" Produced: {work_item}")
            
            # Simulate time between productions
            time.sleep(random.uniform(0.1, 0.3))
        
        print(f"Producer {name} finished")
    
    def consumer(name):
        """Consumes work items (like fulfilling orders)."""
        print(f"Consumer {name} starting...")
        processed_count = 0
        
        while True:
            try:
                # Get work from queue (wait up to 2 seconds)
                work_item = work_queue.get(timeout=2)
                
                # Process the work
                print(f" {name} processing: {work_item}")
                time.sleep(random.uniform(0.2, 0.5))  # Simulate work time
                
                # Mark task as done
                work_queue.task_done()
                processed_count += 1
                
            except queue.Empty:
                # No more work available
                print(f"Consumer {name} finished ({processed_count} items processed)")
                break
    
    # Start producer and consumer threads
    producer_thread = threading.Thread(target=producer, args=("OrderTaker", 8))
    consumer_thread = threading.Thread(target=consumer, args=("Worker",))
    
    producer_thread.start()
    consumer_thread.start()
    
    # Wait for both to complete
    producer_thread.join()
    consumer_thread.join()
    
    print("All work completed!")

print("=== Basic Producer-Consumer Example ===")
simple_producer_consumer()
