import os
import subprocess
from pathlib import Path
import csv

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

# Prepare CSV file
file_exists = os.path.isfile("video_quality_metrics.csv")
with open('video_quality_metrics.csv', 'w', newline='') as csvfile:
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
                decoded_video_file_path = decoded_videos_folder_path / f'{raw_video_name}_decoded_{codec}.yuv'
                subprocess.run(['ffmpeg', '-i', str(encoded_video_file_path), '-c:v', 'rawvideo', '-pix_fmt', 'yuv420p', str(decoded_video_file_path)])

                writer2.writerow([raw_video_name, codec, '', '', '', raw_video_file_size_gb, encoded_video_file_size_gb, change_file_size_gb, '', '', ''])