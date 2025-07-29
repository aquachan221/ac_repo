import os
import subprocess

ffmpeg_path = "D:/aqua/code/dependencies/ffmpeg-2025-07-01-git-11d1b71c31-essentials_build/bin/ffmpeg.exe"
folder_path = "D:/aqua/code/misc/diplomacy"

for filename in os.listdir(folder_path):
    if filename.lower().endswith(".heic"):
        heic_path = os.path.join(folder_path, filename)
        jpg_path = os.path.join(folder_path, os.path.splitext(filename)[0] + ".jpg")

        result = subprocess.run([
            ffmpeg_path,
            "-y",
            "-i", heic_path,
            "-qscale:v", "2",
            "-pix_fmt", "yuvj420p",
            jpg_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0 and os.path.exists(jpg_path):
            print(f"{filename}")
        else:
            print(f"{filename}")
            print(result.stderr.decode())