# import os
# import psutil
# import time
# import csv
# from multiprocessing import Process, Event, Value
# from pathlib import Path
# import subprocess

# ffmpeg_pid = Value('i', 0)

# original_videos_relative_path = 'videos/0_original_videos'
# raw_videos_relative_path = 'videos/1_raw_videos'
# encoded_videos_relative_path = 'videos/2_encoded_videos'
# decoded_videos_relative_path = 'videos/3_decoded_videos'

# # Get the directory of the current script.
# current_path = Path(__file__).parent

# # Build a path to the desired file relative to the script's directory.
# raw_videos_folder_path = current_path / raw_videos_relative_path
# encoded_videos_folder_path = current_path / encoded_videos_relative_path

# # Lists
# codecs = ['mjpeg', 'libx264']

# def encode(stop_event, raw_video_file_path, codec, encoded_video_file_path):
#     print("-" * 150 + "\n" + "Commencing encoding..." + "\n" + "-" * 150)
#     print("-" * 50 + "\n" + codec + "\n" + "-" * 50)
#     subprocess.run(['ffmpeg', '-i', str(raw_video_file_path), '-c:v', codec, str(encoded_video_file_path)])
#     print("-" * 150 + "\n" + "Encoding completed." + "\n" + "-" * 150)
#     stop_event.set()

# def monitor_usage(stop_event, raw_video_name, codec, csv_file_path):
#     print("å" * 150 + "\n" + "Commencing monitoring..." + "\n" + "å" * 150)
#     file_exists = os.path.isfile(csv_file_path)
#     with open(csv_file_path, 'a', newline='') as file:
#         writer = csv.writer(file)

#         if not file_exists:
#             writer.writerow(["Video name", "Codec", "Timestamp", "CPU_Usage(%)", "Memory_Usage(MB)"])
        
#         while not stop_event.is_set():
#             timestamp = time.time()
#             cpu_usage = psutil.cpu_percent(interval=0)
#             process = psutil.Process(os.getpid())
#             memory_usage_mb = process.memory_info().rss / (2**20)
            
#             writer.writerow([raw_video_name, codec, timestamp, cpu_usage, memory_usage_mb])
#             time.sleep(0.2)

#     print("å" * 150 + "\n" + "Monitoring complete." + "\n" + "å" * 150)

# if __name__ == "__main__":
#     stop_event = Event()

#     for raw_video_file in os.listdir(raw_videos_folder_path):
#         if raw_video_file.endswith(('.mp4', '.avi', '.mov', '.mkv')):  # or other video extensions you might use
#             raw_video_name = os.path.splitext(raw_video_file)[0]
#             raw_video_name = raw_video_name.replace("_raw", "")
#             raw_video_file_path = raw_videos_folder_path / raw_video_file

#             # video_resolutions[raw_video_name] = get_video_resolution(raw_video_file_path)
#             # video_frame_rates[raw_video_name] = get_frame_rate(raw_video_file_path)

#             raw_video_file_size = os.path.getsize(raw_video_file_path)
#             raw_video_file_size_gb = round(raw_video_file_size / (2**30), 3)
#             print(raw_video_name)
#             # print(video_resolutions[raw_video_name])
#             # print(type(video_resolutions[raw_video_name]))

#             for codec in codecs:
#                 encoded_video_file_path = encoded_videos_folder_path / f'{raw_video_name}_encoded_{codec}.avi'

#                 # Start encoding and monitoring processes
#                 encoding_process = Process(target=encode, args=(stop_event, raw_video_file_path, codec, encoded_video_file_path))
#                 monitoring_process = Process(target=monitor_usage, args=(stop_event, raw_video_name, codec, "resource_usage.csv"))
                
#                 encoding_process.start()
#                 monitoring_process.start()
                
#                 # Wait for encoding to finish (replace with your condition)
#                 encoding_process.join()

#                 # Once encoding is done, signal the monitor to stop and wait for it
#                 # stop_event.set()
#                 monitoring_process.join()

#                 # Clear the stop_event for the next round of encoding
#                 stop_event.clear()

#                 # print("=" * 150 + "\n" + "=" * 150 + "\n" + "Encoding and monitoring completed." + "\n" + "=" * 150 + "\n" + "=" * 150)
#                 print("=" * 150 + "\n" + "Encoding and monitoring completed." + "\n" + "=" * 150)

#     print("All videos and codecs completed.")

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# import os
# import psutil
# import time
# import csv
# from multiprocessing import Process, Event, Value
# from pathlib import Path
# import subprocess

# ffmpeg_pid = Value('i', 0)

# original_videos_relative_path = 'videos/0_original_videos'
# raw_videos_relative_path = 'videos/1_raw_videos'
# encoded_videos_relative_path = 'videos/2_encoded_videos'
# decoded_videos_relative_path = 'videos/3_decoded_videos'

# # Get the directory of the current script.
# current_path = Path(__file__).parent

# # Build a path to the desired file relative to the script's directory.
# raw_videos_folder_path = current_path / raw_videos_relative_path
# encoded_videos_folder_path = current_path / encoded_videos_relative_path

# # Lists
# codecs = ['mjpeg', 'libx264']

# def encode(stop_event, raw_video_file_path, codec, encoded_video_file_path):
#     print("-" * 150 + "\n" + "Commencing encoding..." + "\n" + "-" * 150)
#     print("-" * 50 + "\n" + codec + "\n" + "-" * 50)
#     encoding_process = subprocess.Popen(['ffmpeg', '-i', str(raw_video_file_path), '-c:v', codec, str(encoded_video_file_path)])
#     encoding_process.wait()
#     print("-" * 150 + "\n" + "Encoding completed." + "\n" + "-" * 150)
#     stop_event.set()

# def monitor_usage(stop_event, raw_video_name, codec, csv_file_path):
#     print("å" * 150 + "\n" + "Commencing monitoring..." + "\n" + "å" * 150)
#     file_exists = os.path.isfile(csv_file_path)
#     with open(csv_file_path, 'a', newline='') as file:
#         writer = csv.writer(file)

#         if not file_exists:
#             writer.writerow(["Video name", "Codec", "Timestamp", "CPU_Usage(%)", "Memory_Usage(MB)"])
        
#         while not stop_event.is_set():
#             timestamp = time.time()
#             cpu_usage = psutil.cpu_percent(interval=0)
#             process = psutil.Process(os.getpid())
#             memory_usage_mb = process.memory_info().rss / (2**20)
            
#             writer.writerow([raw_video_name, codec, timestamp, cpu_usage, memory_usage_mb])
#             time.sleep(0.2)

#     print("å" * 150 + "\n" + "Monitoring complete." + "\n" + "å" * 150)

# if __name__ == "__main__":
#     stop_event = Event()

#     for raw_video_file in os.listdir(raw_videos_folder_path):
#         if raw_video_file.endswith(('.mp4', '.avi', '.mov', '.mkv')):  # or other video extensions you might use
#             raw_video_name = os.path.splitext(raw_video_file)[0]
#             raw_video_name = raw_video_name.replace("_raw", "")
#             raw_video_file_path = raw_videos_folder_path / raw_video_file

#             # video_resolutions[raw_video_name] = get_video_resolution(raw_video_file_path)
#             # video_frame_rates[raw_video_name] = get_frame_rate(raw_video_file_path)

#             raw_video_file_size = os.path.getsize(raw_video_file_path)
#             raw_video_file_size_gb = round(raw_video_file_size / (2**30), 3)
#             print(raw_video_name)
#             # print(video_resolutions[raw_video_name])
#             # print(type(video_resolutions[raw_video_name]))

#             for codec in codecs:
#                 encoded_video_file_path = encoded_videos_folder_path / f'{raw_video_name}_encoded_{codec}.avi'

#                 # Start encoding and monitoring processes
#                 encoding_process = Process(target=encode, args=(stop_event, raw_video_file_path, codec, encoded_video_file_path))
#                 monitoring_process = Process(target=monitor_usage, args=(stop_event, raw_video_name, codec, "resource_usage.csv"))
                
#                 encoding_process.start()
#                 monitoring_process.start()
                
#                 # Wait for encoding to finish (replace with your condition)
#                 encoding_process.join()

#                 # Once encoding is done, signal the monitor to stop and wait for it
#                 # stop_event.set()
#                 monitoring_process.join()

#                 # Clear the stop_event for the next round of encoding
#                 stop_event.clear()

#                 # print("=" * 150 + "\n" + "=" * 150 + "\n" + "Encoding and monitoring completed." + "\n" + "=" * 150 + "\n" + "=" * 150)
#                 print("=" * 150 + "\n" + "Encoding and monitoring completed." + "\n" + "=" * 150)

#     print("All videos and codecs completed.")

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

import os
import psutil
import time
import csv
from multiprocessing import Process, Event, Value
from pathlib import Path
import subprocess

encoding_pid_value = Value('i', 0)

original_videos_relative_path = 'videos/0_original_videos'
raw_videos_relative_path = 'videos/1_raw_videos'
encoded_videos_relative_path = 'videos/2_encoded_videos'
decoded_videos_relative_path = 'videos/3_decoded_videos'

# Get the directory of the current script.
current_path = Path(__file__).parent

# Build a path to the desired file relative to the script's directory.
raw_videos_folder_path = current_path / raw_videos_relative_path
encoded_videos_folder_path = current_path / encoded_videos_relative_path

# Lists
codecs = ['mjpeg', 'libx264']

def encode(stop_event, raw_video_file_path, codec, encoded_video_file_path, encoding_pid_value):
    print("-" * 150 + "\n" + "Commencing encoding..." + "\n" + "-" * 150)
    print("-" * 50 + "\n" + codec + "\n" + "-" * 50)
    start_time_encode = time.time()
    encoding_process = subprocess.Popen(['ffmpeg', '-i', str(raw_video_file_path), '-c:v', codec, str(encoded_video_file_path)])
    encoding_pid_value.value = encoding_process.pid
    encoding_process.wait()
    end_time_encode = time.time()
    file_exists = os.path.isfile("video_quality_metrics.csv")
    with open('video_quality_metrics.csv', 'a', newline='') as csvfile:
        writer2 = csv.writer(csvfile)
        if not file_exists:
            writer2.writerow(['Name of original video', 'Compression Codec', 'Encoding time', 'CPU usage', 'Memory usage', 'Original raw file size', 'Encoded file size', 'Change in file size', 'PSNR', 'SSIM', 'VMAF'])

        encoding_time = end_time_encode - start_time_encode
        writer2.writerow(['', '', encoding_time, '', '', '', '', '', '', '', ''])

    print("-" * 150 + "\n" + str(encoding_pid_value.value) + "\n" + "-" * 150)
    print("-" * 150 + "\n" + "Encoding completed." + "\n" + "-" * 150)
    # encoding_process.communicate()
    stop_event.set()

def monitor_usage(stop_event, raw_video_name, codec, csv_file_path, pid):
    print("å" * 150 + "\n" + "Commencing monitoring..." + "\n" + "å" * 150)
    encoding_process = psutil.Process(pid)
    file_exists = os.path.isfile(csv_file_path)
    with open(csv_file_path, 'a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Video name", "Codec", "Timestamp", "CPU_Usage(%)", "Memory_Usage(MB)"])
        
        while not stop_event.is_set():
            timestamp = time.time()
            cpu_usage = encoding_process.cpu_percent(interval=0)
            memory_usage_mb = encoding_process.memory_info().rss / (2**20)
            
            writer.writerow([raw_video_name, codec, timestamp, cpu_usage, memory_usage_mb])
            time.sleep(0.2)

    print("å" * 150 + "\n" + "Monitoring complete." + "\n" + "å" * 150)

if __name__ == "__main__":
    stop_event = Event()

    for raw_video_file in os.listdir(raw_videos_folder_path):
        if raw_video_file.endswith(('.mp4', '.avi', '.mov', '.mkv')):  # or other video extensions you might use
            raw_video_name = os.path.splitext(raw_video_file)[0]
            raw_video_name = raw_video_name.replace("_raw", "")
            raw_video_file_path = raw_videos_folder_path / raw_video_file

            raw_video_file_size = os.path.getsize(raw_video_file_path)
            raw_video_file_size_gb = round(raw_video_file_size / (2**30), 3)
            print(raw_video_name)

            for codec in codecs:
                encoded_video_file_path = encoded_videos_folder_path / f'{raw_video_name}_encoded_{codec}.avi'

                # Start encoding and monitoring processes
                encoding_process = Process(target=encode, args=(stop_event, raw_video_file_path, codec, encoded_video_file_path, encoding_pid_value))
                encoding_process.start()

                while encoding_pid_value.value == 0:
                    print("No PID detected")
                    time.sleep(0.1)

                print("PID = " + str(encoding_pid_value.value))

                monitoring_process = Process(target=monitor_usage, args=(stop_event, raw_video_name, codec, "resource_usage.csv", encoding_pid_value.value))
                monitoring_process.start()
                
                # Wait for encoding to finish (replace with your condition)
                encoding_process.join()
                monitoring_process.join()

                # Clear the stop_event for the next round of encoding
                stop_event.clear()
                encoding_pid_value.value = 0

                # print("=" * 150 + "\n" + "=" * 150 + "\n" + "Encoding and monitoring completed." + "\n" + "=" * 150 + "\n" + "=" * 150)
                print("=" * 150 + "\n" + "Encoding and monitoring completed." + "\n" + "=" * 150)

    print("All videos and codecs completed.")