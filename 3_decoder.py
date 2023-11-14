"""
This script does the following:
1) Take in encoded videos
2) Decode them into raw format
3) Compare them with the original raw videos based on the following metrics:
    - File size
    - PSNR value
    - SSIM value
    - VMAF value

Note that the calculation of VMAF value still does not work here
"""

import os
import subprocess
from pathlib import Path
import csv
import re

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

def average_value_extractor(cmd_line_output):
    if "PSNR" in cmd_line_output:
        match = re.search(r'average:(\d+\.\d+)', cmd_line_output)
    elif "SSIM" in cmd_line_output:
        match = re.search(r'All:(\d+\.\d+)', cmd_line_output)

    if match:
        ave_value_float = match.group(1)  # This is a string
        ave_value_str = float(ave_value_float)  # Convert to float
        return ave_value_str

# Prepare CSV file
file_exists = os.path.isfile("data_from_decoding.csv")
with open('data_from_decoding.csv', 'w', newline='') as csvfile:
    writer2 = csv.writer(csvfile)
    if not file_exists:
        writer2.writerow(col_names)

    for raw_video_file in os.listdir(raw_videos_folder_path):
        if raw_video_file.endswith(('.mp4', '.avi', '.mov', '.mkv')):  # or other video extensions you might use
            raw_video_name = os.path.splitext(raw_video_file)[0]
            raw_video_name = raw_video_name.replace("_raw", "")
            raw_video_file_path = raw_videos_folder_path / raw_video_file

            raw_video_file_size = os.path.getsize(raw_video_file_path)
            raw_video_file_size_gb = round(raw_video_file_size / (2**30), 3)

            print("\n" + "\n" + raw_video_name + "\n" + "\n")

            for codec in codecs:
                # Encoding
                encoded_video_file_path = encoded_videos_folder_path / f'{raw_video_name}_encoded_{codec}.avi'

                # Calculate size of encoded video file
                encoded_video_file_size = os.path.getsize(encoded_video_file_path)
                encoded_video_file_size_gb = round(encoded_video_file_size / (2**30), 3)

                # Calculate change in size
                change_file_size_gb = raw_video_file_size_gb - encoded_video_file_size_gb

                # Decoding
                decoded_video_file_path = decoded_videos_folder_path / f'{raw_video_name}_decoded_{codec}.avi'
                subprocess.run(['ffmpeg', '-i', str(encoded_video_file_path), '-c:v', 'rawvideo', '-pix_fmt', 'yuv420p', str(decoded_video_file_path)])

                psnr_cmd = ["ffmpeg", "-i", raw_video_file_path, "-i", decoded_video_file_path, "-lavfi", "psnr", "-f", "null", "-"]
                ssim_cmd = ["ffmpeg", "-i", raw_video_file_path, "-i", decoded_video_file_path, "-lavfi", "ssim", "-f", "null", "-"]
                vmaf_cmd = [
                    "ffmpeg",
                    "-i", decoded_video_file_path,
                    "-i", raw_video_file_path,
                    "-filter_complex", "libvmaf",
                    "-f", "null", "-"
                ]
                
                psnr_result = subprocess.run(psnr_cmd, capture_output=True, text=True)
                ssim_result = subprocess.run(ssim_cmd, capture_output=True, text=True)
                vmaf_result = subprocess.run(vmaf_cmd, capture_output=True, text=True)

                psnr_value = average_value_extractor(psnr_result.stderr.split('\n')[-2])
                ssim_value = average_value_extractor(ssim_result.stderr.split('\n')[-2])
                vmaf_value = vmaf_result.stderr.split('\n')[-2]

                writer2.writerow([raw_video_name, codec, '', '', '', raw_video_file_size_gb, encoded_video_file_size_gb, change_file_size_gb, psnr_value, ssim_value, vmaf_value])