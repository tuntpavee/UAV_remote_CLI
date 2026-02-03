import requests
import time
import os

def send_file(path, url):
    if not os.path.exists(path):
        print("File not found.")
        return

    file_size = os.path.getsize(path) / (1024 * 1024)
    print(f"Uploading {path} ({file_size:.2f} MB)...")

    start_time = time.perf_counter()
    
    with open(path, "rb") as f:
        # 'files' handles the multipart/form-data encoding
        response = requests.post(url, files={"file": f})
    
    end_time = time.perf_counter()
    total_time = end_time - start_time

    if response.status_code == 200:
        data = response.json()
        print("\n--- Transfer Summary ---")
        print(f"Server-side write time: {data['duration_seconds']}s")
        print(f"Total Network RTT:      {total_time:.4f}s")
        print(f"Average Speed:          {file_size / total_time:.2f} MB/s")
    else:
        print(f"Error: {response.text}")

# Replace with your Ubuntu IP
target_url = "http://192.168.1.X:8000/upload/" 
send_file("your_large_file.zip", target_url)
