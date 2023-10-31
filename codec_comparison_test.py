import os
import psutil
import time
import csv
from multiprocessing import Process, Event
from pathlib import Path
import subprocess

original_videos_relative_path = 'videos/0_original_videos'
raw_videos_relative_path = 'videos/1_raw_videos'
encoded_videos_relative_path = 'videos/2_encoded_videos'
decoded_videos_relative_path = 'videos/3_decoded_videos'

# Get the directory of the current script.
current_path = Path(__file__).parent

# Build a path to the desired file relative to the script's directory.
raw_videos_folder_path = current_path / raw_videos_relative_path
encoded_videos_folder_path = current_path / encoded_videos_relative_path
decoded_videos_folder_path = current_path / decoded_videos_relative_path

# Lists
# codecs = ['mjpeg', 'libx264', 'libx265']
codecs = ['mjpeg', 'libx264']
col_names = ['Name of original video', 'Compression Codec', 'Encoding time', 'Decoding time', 'CPU usage', 'Memory usage', 'Original raw file size', 'Encoded file size', 'Change in file size', 'PSNR', 'SSIM', 'VMAF']

# Video resolutions
video_resolutions = {}
video_frame_rates = {}

def simulate_encoding(stop_event, raw_video_file_path, codec, encoded_video_file_path):
    # Replace this with your actual encoding logic
    while not stop_event.is_set():
        # time.sleep(0.1)
        subprocess.run(['ffmpeg', '-i', str(raw_video_file_path), '-c:v', codec, str(encoded_video_file_path)])

def monitor_usage(stop_event, raw_video_name, codec, csv_file_path):
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Video name", "Codec", "Timestamp", "CPU_Usage(%)", "Memory_Usage(MB)"])
        
        while not stop_event.is_set():
            timestamp = time.time()
            cpu_usage = psutil.cpu_percent(interval=0)
            process = psutil.Process(os.getpid())
            memory_usage_mb = process.memory_info().rss / (2**20)
            
            writer.writerow([raw_video_name, codec, timestamp, cpu_usage, memory_usage_mb])
            time.sleep(0.2)

if __name__ == "__main__":
    stop_event = Event()

    for raw_video_file in os.listdir(raw_videos_folder_path):
        if raw_video_file.endswith(('.mp4', '.avi', '.mov', '.mkv')):  # or other video extensions you might use
            raw_video_name = os.path.splitext(raw_video_file)[0]
            raw_video_name = raw_video_name.replace("_raw", "")
            raw_video_file_path = raw_videos_folder_path / raw_video_file

            # video_resolutions[raw_video_name] = get_video_resolution(raw_video_file_path)
            # video_frame_rates[raw_video_name] = get_frame_rate(raw_video_file_path)

            raw_video_file_size = os.path.getsize(raw_video_file_path)
            raw_video_file_size_gb = round(raw_video_file_size / (2**30), 3)
            print(raw_video_name)
            print(video_resolutions[raw_video_name])
            print(type(video_resolutions[raw_video_name]))

            for codec in codecs:
                encoded_video_file_path = encoded_videos_folder_path / f'{raw_video_name}_encoded_{codec}.avi'

                # Start encoding and monitoring processes
                encoding_process = Process(target=simulate_encoding, args=(stop_event, raw_video_file_path, codec, encoded_video_file_path))
                monitoring_process = Process(target=monitor_usage, args=(stop_event, raw_video_name, codec, "resource_usage.csv"))
                
                encoding_process.start()
                monitoring_process.start()
                
                # Wait for encoding to finish (replace with your condition)
                encoding_process.join()

                # Once encoding is done, signal the monitor to stop and wait for it
                stop_event.set()
                monitoring_process.join()

    print("Encoding and monitoring completed.")
