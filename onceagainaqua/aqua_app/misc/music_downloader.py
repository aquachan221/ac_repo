import subprocess
import os
import sys

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# === Updated Paths ===
YTDLP_PATH = r'F:\aqua\dependencies\ytdlp\yt-dlp.exe'  # Use the standalone EXE!
FFMPEG_PATH = r'F:\aqua\dependencies\ffmpeg-2025-07-01-git-11d1b71c31-essentials_build\bin\ffmpeg.exe'
OUTPUT_DIR = r'F:\itrmp\music'

# === Get User Input ===
video_url = input("Enter the YouTube URL: ").strip().split("&")[0]  # Strip off playlist junk like &list=, &si=

# === Build Command ===
command = [
    YTDLP_PATH,
    video_url,
    '--no-playlist',  # 💥 Prevent playlist downloads
    '--ffmpeg-location', FFMPEG_PATH,
    '-x',
    '--audio-format', 'mp3',
    '--audio-quality', '0',
    '-o', os.path.join(OUTPUT_DIR, '%(title)s.%(ext)s')
]

# === Run and Handle Errors ===
try:
    if not os.path.isfile(YTDLP_PATH):
        sys.exit("❌ yt-dlp.exe not found. Check your YTDLP_PATH.")
    if not os.path.isfile(FFMPEG_PATH):
        sys.exit("❌ ffmpeg.exe not found. Check your FFMPEG_PATH.")
    subprocess.run(command, check=True)
    print("✅ Download and conversion complete!")
    clear()
except subprocess.CalledProcessError as e:
    print(f"🚨 yt-dlp failed: {e}")
except Exception as ex:
    print(f"⚠️ Unexpected error: {ex}")