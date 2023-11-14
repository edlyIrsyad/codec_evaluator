"""
This script does the following:
1) Take videos from the folder '0_original_videos'
2) Convert them to raw format
3) Save them in the folder '1_raw_videos'
"""

import re
import os
import subprocess
from pathlib import Path

def get_video_resolution(video_path):
    # Command to get video information
    command = ["ffmpeg", "-i", video_path]

    # Run the command and capture the output
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, _ = process.communicate()

    # Decode the output to UTF-8 for string operations
    output = stdout.decode('utf-8')

    # Use regular expression to find the resolution
    match = re.search(r'(\d{2,5})x(\d{2,5})', output)
    if match:
        return match.groups()  # Returns a tuple with (width, height)
    else:
        return None

original_videos_relative_path = 'videos/0_original_videos'
# raw_videos_relative_path = 'videos/1_raw_videos'

# Get the directory of the current script.
current_path = Path(__file__).parent.parent

# Build a path to the desired file relative to the script's directory.
original_videos_folder_path = current_path / original_videos_relative_path
original_video_file = 'kaaholmen_merd6_2018_11_28_17_00_01.mp4'
original_video_name = os.path.splitext(original_video_file)[0]
original_video_file_path = original_videos_folder_path / original_video_file

# Resolution downgrading
output_video_file = f'{original_video_name}_VGA.mp4'
output_video_file_path = original_videos_folder_path / output_video_file
subprocess.run(['ffmpeg', '-i', str(original_video_file_path), '-vf', 'scale=640:480', '-c:a', 'copy', str(output_video_file_path)])

print("\n" + "Downgrading completed." + "\n")

resolution = get_video_resolution(output_video_file_path)

if resolution:
    print(f"The resolution of the video is: {resolution[0]}x{resolution[1]}")
else:
    print("Unable to determine video resolution.")