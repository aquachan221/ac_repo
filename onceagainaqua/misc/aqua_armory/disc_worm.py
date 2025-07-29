import os
import random # type: ignore
import string # type: ignore

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def add_lines():
    nonsense = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(10, 100)))
    with open(__file__, "a") as f:
        f.write(f"\n# {nonsense}")  # Random gibberish added

def stupid():
    file_size = os.path.getsize(__file__)
    print(f"File size: {file_size} bytes")
    clear()

def reallystupid():
    while True:
        add_lines()
        stupid()

reallystupid()