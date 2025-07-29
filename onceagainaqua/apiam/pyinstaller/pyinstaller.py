import subprocess
import sys
import os

# 💧 Customize paths
script_path = r"D:\aqua\code\aqua_app\this_isnt_a_folder\for_the_greater_good\1.py"
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