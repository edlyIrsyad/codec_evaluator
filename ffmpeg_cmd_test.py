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

codec = 'mjpeg'
raw_video_file = 'kaaholmen_merd6_2018_11_28_17_00_01_raw.avi'
raw_video_name = os.path.splitext(raw_video_file)[0]
raw_video_name = raw_video_name.replace("_raw", "")

raw_video_file_path = raw_videos_folder_path / raw_video_file

decoded_video_file_path = decoded_videos_folder_path / f'{raw_video_name}_decoded_{codec}.yuv'

open_video_cmd = ["ffmpeg", "-i", decoded_video_file_path, "-f", "null", "-"]
subprocess.run(open_video_cmd)

# psnr_cmd = ["ffmpeg", "-i", raw_video_file_path, "-i", decoded_video_file_path, "-lavfi", "psnr", "-f", "null", "-"]
# psnr_result = subprocess.run(psnr_cmd, capture_output=True, text=True)
# psnr_value = psnr_result.stderr.split('\n')[-2]

# print('PSNR value = ', end="")
# print(psnr_value)