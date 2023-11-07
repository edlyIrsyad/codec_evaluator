import os
import subprocess
from pathlib import Path
import csv

raw_videos_relative_path = 'videos/1_raw_videos'
encoded_videos_relative_path = 'videos/2_encoded_videos'
decoded_videos_relative_path = 'videos/3_decoded_videos'

# Get the directory of the current script.
script_path = Path(__file__).parent

# Build a path to the desired file relative to the script's directory.
raw_videos_folder_path = script_path / raw_videos_relative_path
encoded_videos_folder_path = script_path / encoded_videos_relative_path
decoded_videos_folder_path = script_path / decoded_videos_relative_path

# Define path to the VMAF model (change to your actual path)
vmaf_model_path = "C:/Users/simen/Desktop/vmaf_float_v0.6.1.pkl"

# List of codecs to test
codecs = ['mjpeg', 'libx264', 'libx265']

# Prepare CSV file
with open('video_quality_metrics.csv', 'w', newline='') as csvfile:
    fieldnames = ['Name of original video', 'Compression Codec', 'Encoding time', 'Decoding time', 'CPU usage', 'Original raw file size', 'Encoded file size', 'Change in file size', 'PSNR', 'SSIM', 'VMAF']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for raw_video_file in os.listdir(raw_videos_folder_path):
        if raw_video_file.endswith(('.mp4', '.avi', '.mov', '.mkv')):  # or other video extensions you might use
            raw_video_name = os.path.splitext(raw_video_file)[0]
            raw_video_input_path = raw_videos_folder_path / raw_video_file
            print(raw_video_input_path)
            print(type(raw_video_input_path))
            raw_video_file_size = os.path.getsize(raw_video_input_path)
            print('Raw video file size: ' + str(raw_video_file_size))

            for codec in codecs:
                # Encoding
                encoded_path = encoded_videos_folder_path / f'{raw_video_name}_encoded_{codec}.avi'
                # subprocess.run(['ffmpeg', '-i', str(raw_video_input_path), '-c:v', codec, str(encoded_path)])

                # Decoding
                decoded_path = decoded_videos_folder_path / f'{raw_video_name}_decoded_{codec}.mp4'
                # subprocess.run(['ffmpeg', '-i', str(encoded_path), '-c:v', codec, str(decoded_path)])

                # Calculate size of encoded video file
                encoded_video_file_size = os.path.getsize(encoded_path)

                # Metrics Calculation
                terminal_input = [
                    "ffmpeg", "-i", raw_video_input_path, "-i", decoded_path, 
                    "-filter_complex",
                    f"psnr;ssim;libvmaf=model_path={vmaf_model_path}",
                    "-an", "-f", "null", "-"
                ]

                # terminal_output = subprocess.check_output(terminal_input, stderr=subprocess.STDOUT, text=True)
                # psnr_value = float(next(line for line in terminal_output.splitlines() if "PSNR" in line).split('average:')[1].strip())
                # ssim_value = float(next(line for line in terminal_output.splitlines() if "SSIM" in line).split('All:')[1].split(' ')[0])
                # vmaf_value = float(next(line for line in terminal_output.splitlines() if "VMAF score" in line).split(':')[1].strip())

                # writer.writerow({
                #     'Name of original video': raw_video_name,
                #     'Compression Codec': codec,
                #     'Original raw file size': raw_video_file_size,
                #     'Encoded file size': encoded_video_file_size,
                #     'Change in file size': encoded_video_file_size - raw_video_file_size,
                #     'PSNR': psnr_value,
                #     'SSIM': ssim_value,
                #     'VMAF': vmaf_value
                # })

                # writer.writerow({
                #     'Name of original video': raw_video_name,
                #     'Compression Codec': codec,
                #     'Original raw file size': raw_video_file_size,
                #     'Encoded file size': encoded_video_file_size,
                #     'Change in file size': encoded_video_file_size - raw_video_file_size,
                #     'PSNR': 54,
                #     'SSIM': 76,
                #     'VMAF': 324
                # })