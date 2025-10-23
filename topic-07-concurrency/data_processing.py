import concurrent.futures
import math
import time

def process_data_chunk(data_info):
    """Process a chunk of data (like analyzing a CSV section)."""
    chunk_id, start_value, size = data_info
    
    print(f"Processing chunk {chunk_id} ({size:,} items)...")
    
    # Simulate data processing: filtering, transforming, aggregating
    processed_items = []
    total_sum = 0
    
    for i in range(size):
        value = start_value + i
        # Simulate complex data transformations
        processed_value = value ** 2 + math.sin(value) * 100
        processed_items.append(processed_value)
        total_sum += processed_value
    
    result = {
        'chunk_id': chunk_id,
        'items_processed': len(processed_items),
        'sum': total_sum,
        'average': total_sum / len(processed_items),
        'min_value': min(processed_items),
        'max_value': max(processed_items)
    }
    
    print(f"Chunk {chunk_id} complete: {result['items_processed']:,} items processed")
    return result

def parallel_data_processing():
    """Process large dataset in parallel chunks."""
    
    # Simulate dividing a large dataset into chunks
    data_chunks = [
        (1, 0, 100_000),      # chunk_id, start_value, size
        (2, 100_000, 100_000),
        (3, 200_000, 100_000),
        (4, 300_000, 100_000),
        (5, 400_000, 100_000)
    ]
    
    print(f"Processing {len(data_chunks)} data chunks in parallel...")
    start_time = time.time()
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        # Submit all chunks for processing
        future_to_chunk = {
            executor.submit(process_data_chunk, chunk_info): chunk_info[0]
            for chunk_info in data_chunks
        }
        
        # Collect and combine results
        all_results = []
        for future in concurrent.futures.as_completed(future_to_chunk):
            chunk_id = future_to_chunk[future]
            try:
                result = future.result()
                all_results.append(result)
            except Exception as e:
                print(f"Chunk {chunk_id} failed: {e}")
    
    processing_time = time.time() - start_time
    
    # Combine results from all chunks
    total_items = sum(r['items_processed'] for r in all_results)
    total_sum = sum(r['sum'] for r in all_results)
    overall_average = total_sum / total_items if total_items > 0 else 0
    
    print(f"\n=== Processing Complete ===")
    print(f"Total time: {processing_time:.2f}s")
    print(f"Total items processed: {total_items:,}")
    print(f"Overall average: {overall_average:.2f}")
    print(f"Processing rate: {total_items/processing_time:,.0f} items/second")
    
    return all_results

# Run parallel data processing
processing_results = parallel_data_processing()
