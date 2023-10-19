import os
import subprocess
from pathlib import Path
import sys
import re
import time
import csv

original_videos_relative_path = 'videos/0_original_videos'
raw_videos_relative_path = 'videos/1_raw_videos'

# Get the directory of the current script.
current_path = Path(__file__).parent

# Build a path to the desired file relative to the script's directory.
original_videos_folder_path = current_path / original_videos_relative_path
raw_videos_folder_path = current_path / raw_videos_relative_path

for original_video_file in os.listdir(original_videos_folder_path):
    if original_video_file.endswith(('.mp4', '.avi', '.mov', '.mkv')):  # or other video extensions you might use
        original_video_name = os.path.splitext(original_video_file)[0]
        original_video_file_path = original_videos_folder_path / original_video_file

        print("-" * 50)
        print("-" * 50)
        print("-" * 50)

        # Rawification
        raw_video_file_path = raw_videos_folder_path / f'{original_video_name}_encoded_raw.avi'
        subprocess.run(['ffmpeg', '-i', str(original_video_file_path), '-c:v', 'rawvideo', str(raw_video_file_path)])