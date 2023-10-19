import os
import subprocess
from pathlib import Path
import sys
import re
import time
import csv

# sys.stdout = open('output.txt', 'w')
# print("This will be written to output.txt")

raw_videos_relative_path = 'videos/1_raw_videos'
encoded_videos_relative_path = 'videos/2_encoded_videos'
decoded_videos_relative_path = 'videos/3_decoded_videos'

# Get the directory of the current script.
script_path = Path(__file__).parent

# Build a path to the desired file relative to the script's directory.
raw_videos_folder_path = script_path / raw_videos_relative_path
encoded_videos_folder_path = script_path / encoded_videos_relative_path
decoded_videos_folder_path = script_path / decoded_videos_relative_path

# List of codecs to test
# codecs = ['mjpeg', 'libx264', 'libx265']
codecs = ['mjpeg', 'libx264']

# Video resolutions
video_resolutions = {}

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

# Prepare CSV file
with open('video_quality_metrics.csv', 'w', newline='') as csvfile:
    fieldnames = ['Name of original video', 'Compression Codec', 'Encoding time', 'Decoding time', 'CPU usage', 'Original raw file size', 'Encoded file size', 'Change in file size', 'PSNR', 'SSIM', 'VMAF']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for video_file in os.listdir(raw_videos_folder_path):
        if video_file.endswith(('.mp4', '.avi', '.mov', '.mkv')):  # or other video extensions you might use
            video_name = os.path.splitext(video_file)[0]
            input_path = raw_videos_folder_path / video_file

            video_resolutions[video_name] = get_video_resolution(input_path)
            raw_video_file_size = os.path.getsize(input_path)

            print("-" * 50)
            print("-" * 50)
            print("-" * 50)
            print(video_name)
            print(video_resolutions[video_name])
            print(type(video_resolutions[video_name]))

            for codec in codecs:
                # Encoding
                encoded_path = encoded_videos_folder_path / f'{video_name}_encoded_{codec}.avi'
                print("-" * 50)
                print(codec)
                # subprocess.run(['ffmpeg', '-i', str(input_path), '-r', get_frame_rate(input_path), '-s', video_resolutions[video_name], '-c:v', codec, '-pix_fmt', get_pixel_format(input_path), str(encoded_path)])
                start_time_encode = time.time()
                subprocess.run(['ffmpeg', '-i', str(input_path), '-c:v', codec, str(encoded_path)])
                end_time_encode = time.time()

                # Calculate size of encoded video file
                encoded_video_file_size = os.path.getsize(encoded_path)

                # Decoding
                decoded_path = decoded_videos_folder_path / f'{video_name}_decoded_{codec}.mp4'
                print("-" * 50)
                print(codec)
                # subprocess.run(['ffmpeg', '-i', str(encoded_path), '-r', get_frame_rate(input_path), '-s', video_resolutions[video_name], '-c:v', codec, '-pix_fmt', get_pixel_format(input_path), str(decoded_path)])
                start_time_decode = time.time()
                subprocess.run(['ffmpeg', '-i', str(encoded_path), '-c:v', codec, str(decoded_path)])
                end_time_decode = time.time()

                encoding_time = end_time_encode - start_time_encode
                decoding_time = end_time_decode - start_time_decode

                writer.writerow({
                    'Name of original video': video_name,
                    'Compression Codec': codec,
                    'Encoding time': encoding_time,
                    'Decoding time': decoding_time,
                    'Original raw file size': raw_video_file_size,
                    'Encoded file size': encoded_video_file_size,
                    'Change in file size': encoded_video_file_size - raw_video_file_size,
                    'PSNR': 54,
                    'SSIM': 76,
                    'VMAF': 324
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