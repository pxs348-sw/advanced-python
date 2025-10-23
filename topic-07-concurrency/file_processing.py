import os
import time
import concurrent.futures

def process_file_simulation(filename):
    """Simulate processing a file (reading, analyzing, etc.)."""
    print(f"Processing {filename}...")
    
    # Simulate I/O operations
    time.sleep(0.5)  # Simulate reading file
    time.sleep(0.3)  # Simulate processing
    time.sleep(0.2)  # Simulate writing results
    
    # Return processing results
    return {
        'filename': filename,
        'lines_processed': len(filename) * 10,  # Fake metric
        'processing_time': 1.0,
        'status': 'completed'
    }

def batch_file_processor(filenames, use_threads=False, max_workers=3):
    """Process multiple files sequentially or with threads."""
    
    start_time = time.time()
    results = []
    
    if use_threads:
        print(f"Processing {len(filenames)} files with {max_workers} threads...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all file processing tasks
            future_to_file = {
                executor.submit(process_file_simulation, filename): filename 
                for filename in filenames
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_file):
                result = future.result()
                results.append(result)
                print(f"   Completed {result['filename']}")
    
    else:
        print(f"Processing {len(filenames)} files sequentially...")
        
        for filename in filenames:
            result = process_file_simulation(filename)
            results.append(result)
            print(f"   Completed {result['filename']}")
    
    total_time = time.time() - start_time
    method = "threaded" if use_threads else "sequential"
    print(f"{method.title()} processing completed in {total_time:.2f}s\n")
    
    return results, total_time

# Test with sample files
sample_files = [
    "data_report_2024.txt",
    "user_logs_january.txt", 
    "sales_summary.txt",
    "inventory_update.txt",
    "customer_feedback.txt"
]

print("Comparing file processing approaches:")
sequential_results, seq_time = batch_file_processor(sample_files, use_threads=False)
threaded_results, thread_time = batch_file_processor(sample_files, use_threads=True, max_workers=3)

speedup = seq_time / thread_time if thread_time > 0 else 0
print(f"File processing speedup: {speedup:.1f}x")
