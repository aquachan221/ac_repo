import subprocess
import sys
import os

# 💧 Customize paths
script_path = r"D:\aqua\repo\ac_repo\onceagainaqua\apiam\sec\aqua_secure.py"
destination_folder = r"D:\aqua\code\apiam\pyinstaller"

# 🧠 Ensure destination exists
os.makedirs(destination_folder, exist_ok=True)

# 🏗️ PyInstaller command with output directory
command = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    f"--distpath={destination_folder}",
    script_path
]

# 🚀 Run build
print(f"created at {destination_folder}")
subprocess.run(command)