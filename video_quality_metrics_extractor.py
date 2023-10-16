import os
import subprocess
from pathlib import Path

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
codecs = ['mjpeg', 'libx264', 'libx265']

for video_file in os.listdir(raw_videos_folder_path):
    if video_file.endswith(('.mp4', '.avi', '.mov', '.mkv')):  # or other video extensions you might use
        video_name = os.path.splitext(video_file)[0]
        input_path = raw_videos_folder_path / video_file
        print(input_path)
        print(type(input_path))

        for codec in codecs:
            # Encoding
            encoded_path = encoded_videos_folder_path / f'{video_name}_encoded_{codec}.avi'
            print(encoded_path)
            print(type(encoded_path))
            subprocess.run(['ffmpeg', '-i', str(input_path), '-c:v', codec, str(encoded_path)])

            # Decoding
            decoded_path = decoded_videos_folder_path / f'{video_file}_decoded_{codec}.mp4'
            subprocess.run(['ffmpeg', '-i', str(encoded_path), '-c:v', codec, str(decoded_path)])