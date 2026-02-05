import requests
import time
import os
from tqdm import tqdm

file_path = '/Users/tunt/Downloads/target.zip'
def send_file_with_progress(path, url):
    file_size = os.path.getsize(path)
    filename = os.path.basename(path)
    
    # Wrap the file in a tqdm progress bar
    with open(path, "rb") as f:
        with tqdm(total=file_size, unit="B", unit_scale=True, desc=filename) as pbar:
            # Custom generator to update progress bar as data is read
            def file_generator():
                while True:
                    chunk = f.read(8192) # Read in 8KB chunks
                    if not chunk:
                        break
                    yield chunk
                    pbar.update(len(chunk))

            start_time = time.perf_counter()
            response = requests.post(url,
				data=file_generator(),
				params={"filename": filename})
            end_time = time.perf_counter()

    duration = end_time - start_time
    if response.status_code == 200:
        res_data = response.json()
        print(f"\n✅ Transfer Complete!")
        print(f"Total Time (RTT): {duration:.2f}s")
        print(f"Server Processing: {res_data['duration_seconds']}s")
    else:
        print(f"\n❌ Error: {response.status_code}")

# Run this on your Mac
target_url = "http://192.168.0.120:8000/upload/"
send_file_with_progress(file_path, target_url)
