import subprocess
import threading
import sys

def read_stdin():
    print("[🔄 Listening to standard input...]")
    for line in sys.stdin:
        print(f"[STDIN] {line.strip()}")

def run_external(cmd):
    print(f"[⚙️ Running external command: {' '.join(cmd)}]")
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    for line in proc.stdout:
        print(f"[PROCESS] {line.strip()}")

# Start stdin reader
threading.Thread(target=read_stdin, daemon=True).start()
