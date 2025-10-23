import concurrent.futures
import time
import requests

def fetch_url_info(url):
    """Fetch URL and return timing info."""
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        end_time = time.time()
        
        return {
            'url': url,
            'status': response.status_code,
            'time': end_time - start_time,
            'size': len(response.content),
            'success': True
        }
    except Exception as e:
        return {
            'url': url,
            'error': str(e),
            'success': False
        }

def download_sequential_vs_threaded():
    """Compare sequential vs threaded downloads."""
    
    # Test URLs (using httpbin for reliable testing)
    urls = [
        "https://httpbin.org/delay/1",    # 1 second delay
        "https://httpbin.org/delay/1",    # 1 second delay  
        "https://httpbin.org/delay/1",    # 1 second delay
        "https://httpbin.org/json",       # Quick response
        "https://httpbin.org/uuid"        # Quick response
    ]
    
    print("=== Sequential Downloads (One at a Time) ===")
    start_time = time.time()
    sequential_results = []
    
    for url in urls:
        result = fetch_url_info(url)
        sequential_results.append(result)
        status = "" if result['success'] else ""
        print(f"{status} {url}")
    
    sequential_time = time.time() - start_time
    print(f"Sequential total: {sequential_time:.2f}s\n")
    
    print("=== Threaded Downloads (Multiple Workers) ===")
    start_time = time.time()
    threaded_results = []
    
    # The magic: ThreadPoolExecutor manages the threads for us
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all tasks at once
        future_to_url = {executor.submit(fetch_url_info, url): url for url in urls}
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_url):
            result = future.result()
            threaded_results.append(result)
            status = "" if result['success'] else ""
            print(f"{status} {result['url']}")
    
    threaded_time = time.time() - start_time
    print(f"Threaded total: {threaded_time:.2f}s")
    
    speedup = sequential_time / threaded_time if threaded_time > 0 else 0
    print(f"Speedup: {speedup:.1f}x faster!")
    
    return sequential_results, threaded_results

try:
    download_sequential_vs_threaded()
except Exception as e:
    print(f"Network test failed: {e}")
    print("That's okay - the concept is what matters!")

