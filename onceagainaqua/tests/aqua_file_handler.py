import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

# === Global widgets ===
status_var = None
meta_box = None

# === 6-bit character maps ===
main_table = [
    'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',
    'Q','R','S','T','U','V','W','X','Y','Z',
    'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
    'q','r','s','t','u','v','w','x','y','z',
    '0','1','2','3','4','5','6','7','8','9',
    '[ext]','[end]'
]

ext_table = [
    '!','@','#','$','%','^','&','*','(',')',
    '-','_','=','+','[',']','{','}','\\','|',
    ';',':',"'",'"',',','.','<','>','/','?','`','~', ' '
] + [None] * (64 - 31)

# === Aqua file detection config ===
AQUA_FILE_TYPES = {
    '101101 011110 110001 101101 111111': 'Text File',
    '100010 100110 011010 100000 011110 111111': 'Image',
    '111111 000000 111111': 'Metadata Block'
}
DEFAULT_FILE_TYPE = 'Unknown Format'
AUTO_DECODE_AQUA = True

# === Encoding ===
def encode_6bit_with_ext(text):
    result_bits = []
    for char in text:
        if char in main_table:
            result_bits.append(f'{main_table.index(char):06b}')
        elif char in ext_table:
            result_bits.append('111110')  # [ext]
            ext_idx = ext_table.index(char)
            result_bits.append(f'{ext_idx:06b}')
        else:
            result_bits.extend(['111110', '111111'])  # fallback '?'
    result_bits.append('111111')  # [end]
    return ' '.join(result_bits)

# === Decoding ===
def decode_6bit_with_ext(binary_string):
    bits = binary_string.replace(' ', '').replace('\n', '')
    output = []
    i = 0
    in_metadata = False
    marker = '111111 000000 111111'

    while i + 6 <= len(bits):
        # Check for metadata marker
        if bits[i:i+18] == marker:
            in_metadata = not in_metadata  # Toggle metadata mode
            i += 18
            continue

        if in_metadata:
            i += 6
            continue

        chunk = bits[i:i+6]
        idx = int(chunk, 2)
        i += 6

        if idx == 63:  # [end]
            break
        elif idx == 62:  # [ext]
            if i + 6 > len(bits): break
            ext_chunk = bits[i:i+6]
            ext_idx = int(ext_chunk, 2)
            ext_char = ext_table[ext_idx] if 0 <= ext_idx < len(ext_table) else '?'
            output.append(ext_char or '?')
            i += 6
        else:
            char = main_table[idx] if 0 <= idx < len(main_table) else '?'
            output.append(char)

    return ''.join(output)


# === Aqua detection logic ===
def detect_aqua_file_type(content):
    flat = content.strip().replace(' ', '').replace('\n', '')
    for magic, ftype in AQUA_FILE_TYPES.items():
        magic_flat = magic.replace(' ', '')
        if flat.startswith(magic_flat):
            return ftype, len(magic_flat)
    return DEFAULT_FILE_TYPE, 0

# === File loader logic ===
def load_file_from_path(filepath):
    global status_var, meta_box
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        ftype, header_bits = detect_aqua_file_type(content)
        flat = content.strip().replace(' ', '').replace('\n', '')
        header_raw = flat[:header_bits]

        # Display metadata
        meta_box.config(state="normal")
        meta_box.delete("1.0", tk.END)
        meta_box.insert(tk.END, f"File Type: {ftype}\n")
        meta_box.insert(tk.END, f"Header Bits:\n{header_raw}")
        meta_box.config(state="disabled")

        messagebox.showinfo("Aqua File Type", f"{os.path.basename(filepath)}\nDetected: {ftype}")
        text_input.delete("1.0", tk.END)
        text_input.insert(tk.END, content)

        if AUTO_DECODE_AQUA and ftype == 'Text File':
            body = flat[header_bits:]
            decoded = decode_6bit_with_ext(body)
            output.delete("1.0", tk.END)
            output.insert(tk.END, decoded)

        status_var.set(f"Loaded: {os.path.basename(filepath)} ({ftype})")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_var.set("Failed to load file.")

# === Aqua file writer ===
def write_aqua_file():
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showinfo("No Input", "Please enter text to write to an Aqua file.")
        return
    encoded = encode_6bit_with_ext(text)
    header = "101101 011110 110001 101101 111111"  # Text File header
    aqua_data = f"{header} {encoded}"
    filepath = filedialog.asksaveasfilename(defaultextension=".aqua", title="Save Aqua File")
    if filepath:
        try:
            with open(filepath, 'w') as f:
                f.write(aqua_data)
            messagebox.showinfo("Success", f"Aqua file saved to {filepath}")
            status_var.set(f"Saved Aqua File: {os.path.basename(filepath)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            status_var.set("Failed to save file.")

# === GUI logic ===
def encode_action():
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Missing Input", "Please enter text to encode.")
        return
    bits = encode_6bit_with_ext(text)
    output.delete("1.0", tk.END)
    output.insert(tk.END, bits)
    status_var.set("Text encoded to 6-bit format.")

def decode_action():
    bits = text_input.get("1.0", tk.END).strip()
    if not bits:
        messagebox.showwarning("Missing Input", "Please enter binary data to decode.")
        return
    result = decode_6bit_with_ext(bits)
    output.delete("1.0", tk.END)
    output.insert(tk.END, result)
    status_var.set("Binary stream decoded.")

def save_to_file():
    content = output.get("1.0", tk.END).strip()
    if not content:
        messagebox.showinfo("Nothing to Save", "Output is empty.")
        return
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", title="Save Output")
    if filepath:
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            messagebox.showinfo("Success", f"Saved to {filepath}")
            status_var.set(f"Saved: {os.path.basename(filepath)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            status_var.set("Failed to save file.")

def browse_directory():
    folder = filedialog.askdirectory(title="Choose Directory")
    if folder:
        file_listbox.delete(0, tk.END)
        for file in os.listdir(folder):
            path = os.path.join(folder, file)
            if os.path.isfile(path):
                file_listbox.insert(tk.END, path)
        status_var.set(f"Loaded directory: {folder}")

def on_file_select(event):
    selection = file_listbox.curselection()
    if selection:
        path = file_listbox.get(selection[0])
        load_file_from_path(path)

# === Dark mode styling ===
def apply_dark_mode():
    root.tk_setPalette(background="#1e1e1e", foreground="#e2e2e2", activeBackground="#444", activeForeground="#fff")
    widgets = [text_input, output, frame, btn_frame, explorer_frame, file_listbox, meta_box]
    for widget in widgets:
        try:
            widget.configure(bg="#2e2e2e", fg="#ffffff", insertbackground="#ffffff", selectbackground="#444")
        except tk.TclError:
            widget.configure(bg="#2e2e2e")

# === GUI Layout ===
root = tk.Tk()
root.title("Aqua File Manager & 6-bit Encoder (Dark Mode)")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

explorer_frame = tk.Frame(frame)
explorer_frame.pack(side="left", fill="y", padx=(0, 10))

tk.Button(explorer_frame, text="Browse Folder", command=browse_directory).pack()
file_listbox = tk.Listbox(explorer_frame, height=20, width=40)
file_listbox.pack(fill="y", expand=True, pady=(5, 0))
file_listbox.bind("<Double-Button-1>", on_file_select)

right_pane = tk.Frame(frame)
right_pane.pack(side="left", fill="both", expand=True)

tk.Label(right_pane, text="Input / Binary Stream:").pack(anchor="w")
text_input = scrolledtext.ScrolledText(right_pane, height=8, width=80)
text_input.pack(fill="x", expand=True, pady=(0, 10))

btn_frame = tk.Frame(right_pane)
btn_frame.pack()

tk.Button(btn_frame, text="Encode", width=12, command=encode_action).pack(side="left", padx=4)
tk.Button(btn_frame, text="Decode", width=12, command=decode_action).pack(side="left", padx=4)
tk.Button(btn_frame, text="Save Output", width=12, command=save_to_file).pack(side="left", padx=4)
tk.Button(btn_frame, text="Write Aqua File", width=14, command=write_aqua_file).pack(side="left", padx=4)

tk.Label(right_pane, text="Output:").pack(anchor="w", pady=(10, 0))
output = scrolledtext.ScrolledText(right_pane, height=8, width=80)
output.pack(fill="x", expand=True)

# === Metadata Sidebar ===
meta_label = tk.Label(frame, text="Header Metadata:")
meta_label.pack(side="right", anchor="ne", padx=(5, 10))
meta_box = scrolledtext.ScrolledText(frame, height=6, width=30, state="disabled", wrap="word")
meta_box.pack(side="right", fill="y", padx=(0, 10), pady=(0, 30))

# === Status Bar ===
status_var = tk.StringVar()
status_var.set("Ready.")
status_bar = tk.Label(root, textvariable=status_var, bd=1, relief="sunken", anchor="w", bg="#2e2e2e", fg="#ffffff")
status_bar.pack(side="bottom", fill="x")

apply_dark_mode()
root.mainloop()