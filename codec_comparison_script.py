import os
import subprocess
from pathlib import Path

relative_path = 'videos/1_raw_videos'

# Get the directory of the current script.
script_dir = Path(__file__).parent

# Build a path to the desired file relative to the script's directory.
raw_videos_file_path = script_dir / relative_path

print()
print('Raw videos file path: ')
print(raw_videos_file_path)
print()