import os
import subprocess
from pathlib import Path
import sys
import re
import time
import csv
import psutil
from multiprocessing import Process, Event 

# sys.stdout = open('output.txt', 'w')
# print("This will be written to output.txt")

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
col_names = ['Name of original video', 'Compression Codec', 'Encoding time', 'CPU usage', 'Memory usage', 'Original raw file size', 'Encoded file size', 'Change in file size', 'PSNR', 'SSIM', 'VMAF']

# Video resolutions
video_resolutions = {}
video_frame_rates = {}

# Function definitions
def get_raw_video_name():
    return 0

def get_video_resolution(video_path):
    cmd = ['ffmpeg', '-i', video_path]
    sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = sp.communicate()
    lines = err.decode().split('\n')
    for line in lines:
        if 'Stream' in line and 'Video' in line:
            match = re.search(r'(\d{2,5}x\d{2,5})', line)
            if match:
                return match.group(0)
    return None

def get_frame_rate(video_path):
    # Use ffprobe to obtain video frame rate
    cmd = [
        'ffprobe', 
        '-v', 'error', 
        '-select_streams', 'v:0', 
        '-show_entries', 'stream=r_frame_rate',
        '-of', 'default=noprint_wrappers=1:nokey=1', 
        video_path
    ]

    frame_rate = subprocess.check_output(cmd, universal_newlines=True).strip()
    return frame_rate

def get_pixel_format(video_path):
    # Use ffprobe to obtain video pixel format
    cmd = [
        'ffprobe', 
        '-v', 'error', 
        '-select_streams', 'v:0', 
        '-show_entries', 'stream=pix_fmt',
        '-of', 'default=noprint_wrappers=1:nokey=1', 
        video_path
    ]
    
    pixel_format = subprocess.check_output(cmd, universal_newlines=True).strip()
    return pixel_format

def encode():
    return 0

def decode():
    return 0

def monitor_resource_usage():
    return 0

if __name__ == "__main__":
    stop_event = Event()

    # Prepare CSV file
    with open('video_quality_metrics.csv', 'w', newline='') as csvfile:
        results_csv = csv.DictWriter(csvfile, fieldnames=col_names)
        results_csv.writeheader()

        for raw_video_file in os.listdir(raw_videos_folder_path):
            if raw_video_file.endswith(('.mp4', '.avi', '.mov', '.mkv')):  # or other video extensions you might use
                raw_video_name = os.path.splitext(raw_video_file)[0]
                raw_video_name = raw_video_name.replace("_raw", "")
                raw_video_file_path = raw_videos_folder_path / raw_video_file

                video_resolutions[raw_video_name] = get_video_resolution(raw_video_file_path)
                video_frame_rates[raw_video_name] = get_frame_rate(raw_video_file_path)

                raw_video_file_size = os.path.getsize(raw_video_file_path)
                raw_video_file_size_gb = round(raw_video_file_size / (2**30), 3)

                print("-" * 50)
                print("-" * 50)
                print("-" * 50)
                print(raw_video_name)
                print(video_resolutions[raw_video_name])
                print(type(video_resolutions[raw_video_name]))

                for codec in codecs:
                    # Encoding
                    encoded_video_file_path = encoded_videos_folder_path / f'{raw_video_name}_encoded_{codec}.avi'
                    print("-" * 50)
                    print(codec)
                    # subprocess.run(['ffmpeg', '-i', str(input_path), '-r', get_frame_rate(input_path), '-s', video_resolutions[video_name], '-c:v', codec, '-pix_fmt', get_pixel_format(input_path), str(encoded_path)])
                    start_time_encode = time.time()
                    # subprocess.run(['ffmpeg', '-i', str(raw_video_file_path), '-c:v', codec, str(encoded_video_file_path)])
                    encoding_process = subprocess.Popen(['ffmpeg', '-i', str(raw_video_file_path), '-c:v', codec, str(encoded_video_file_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    end_time_encode = time.time()

                    # Get PID of the encoding process
                    encoding_pid = encoding_process.pid
                    encoding_psutil_process = psutil.Process(encoding_pid)

                    # List to collect CPU usage and memory usage (RSS) over time
                    cpu_usages = []
                    mem_usages = []

                    # Continuously measure the CPU usage during the encoding process
                    while encoding_process.poll() is None:  # While the process is running
                        cpu_usages.append(encoding_psutil_process.cpu_percent(interval=0.2))  # Measure the CPU usage every second
                        mem_usages.append(encoding_psutil_process.memory_info().rss / (1024 ** 2))  # Get RSS in MB

                    # Finish when the encoding process is complete
                    _, _ = encoding_process.communicate()

                    ave_cpu_usage = sum(cpu_usages) / len(cpu_usages)
                    ave_mem_usage = sum(mem_usages) / len(mem_usages)

                    # Calculate size of encoded video file
                    encoded_video_file_size = os.path.getsize(encoded_video_file_path)
                    encoded_video_file_size_gb = round(encoded_video_file_size / (2**30), 3)

                    # Decoding
                    decoded_video_file_path = decoded_videos_folder_path / f'{raw_video_name}_decoded_{codec}.yuv'
                    print("-" * 50)
                    print(codec)
                    # subprocess.run(['ffmpeg', '-i', str(encoded_path), '-r', get_frame_rate(input_path), '-s', video_resolutions[video_name], '-c:v', codec, '-pix_fmt', get_pixel_format(input_path), str(decoded_path)])
                    start_time_decode = time.time()
                    subprocess.run(['ffmpeg', '-i', str(encoded_video_file_path), "-s", video_resolutions[raw_video_name], '-c:v', 'rawvideo', '-r', video_frame_rates[raw_video_name], '-pix_fmt', 'yuv420p', str(decoded_video_file_path)])
                    end_time_decode = time.time()

                    encoding_time = end_time_encode - start_time_encode
                    decoding_time = end_time_decode - start_time_decode

                    # Capturing CPU and memory utilization
                    process = psutil.Process(os.getpid())
                    cpu_usage = process.cpu_percent(interval=0.2)
                    mem_usage = process.memory_info().rss / (1024 * 1024)  # in MB

                    results_csv.writerow({
                        'Name of original video': raw_video_name,
                        'Compression Codec': codec,
                        'Encoding time': encoding_time,
                        'Decoding time': decoding_time,
                        'CPU usage': ave_cpu_usage,
                        'Memory usage': ave_mem_usage,
                        'Original raw file size': raw_video_file_size_gb,
                        'Encoded file size': encoded_video_file_size_gb,
                        'Change in file size': round(encoded_video_file_size_gb - raw_video_file_size_gb, 3),
                        'PSNR': 54,
                        'SSIN': 63,
                        'VMAF': 7845
                        })
                
# print()
# print('Raw videos folder path: ')
# print(raw_videos_folder_path)
# print(type(raw_videos_folder_path))
# print()

# List all files in the directory
# files = [f for f in os.listdir(raw_videos_folder_path) if os.path.isfile(os.path.join(raw_videos_folder_path, f))]

# print('List of files:')

# for file in files:
#     base_name = os.path.splitext(file)[0]
#     print(base_name)
#     print(type(base_name))