import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

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
    ';',':',"'",'"',',','.','<','>','/','?','`','~'
] + [None] * (64 - 32)


# === Encoding ===
def encode_6bit_with_ext(text):
    bits = []
    for char in text:
        if char in main_table:
            idx = main_table.index(char)
            bits.append(f'{idx:06b}')
        elif char in ext_table:
            bits.append(f'{62:06b}')
            bits.append(f'{ext_table.index(char):06b}')
        else:
            continue
    bits.append(f'{63:06b}')
    return ' '.join(bits)  # ← this is the correct join

# === Decoding ===
def decode_6bit_with_ext(binary_string):
    binary_string = binary_string.replace(' ', '').replace('\n', '')
    chunks = [binary_string[i:i+6] for i in range(0, len(binary_string), 6)]

    output = []
    i = 0
    while i < len(chunks):
        if len(chunks[i]) < 6:
            break
        idx = int(chunks[i], 2)
        if idx == 63:
            break
        elif idx == 62:
            i += 1
            if i >= len(chunks): break
            ext_idx = int(chunks[i], 2)
            ext_char = ext_table[ext_idx] if ext_idx < len(ext_table) else '?'
            output.append(ext_char or '?')
        else:
            output.append(main_table[idx] if idx < len(main_table) else '?')
        i += 1

    return ''.join(output)

# === GUI logic ===
def encode_action():
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Missing Input", "Please enter text to encode.")
        return
    bits = encode_6bit_with_ext(text)
    output.delete("1.0", tk.END)
    output.insert(tk.END, bits)

def decode_action():
    bits = text_input.get("1.0", tk.END).strip()
    if not bits:
        messagebox.showwarning("Missing Input", "Please enter binary data to decode.")
        return
    result = decode_6bit_with_ext(bits)
    output.delete("1.0", tk.END)
    output.insert(tk.END, result)

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
        except Exception as e:
            messagebox.showerror("Error", str(e))

def load_from_file():
    filepath = filedialog.askopenfilename(title="Open Input File", filetypes=[("Text files", "*.txt")])
    if filepath:
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            text_input.delete("1.0", tk.END)
            text_input.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("Error", str(e))


# === Tkinter GUI ===
root = tk.Tk()
root.title("6-bit Encoder/Decoder (with [ext] Support)")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="Input / Binary Stream:").pack(anchor="w")
text_input = scrolledtext.ScrolledText(frame, height=8, width=80)
text_input.pack(fill="x", expand=True, pady=(0, 10))

btn_frame = tk.Frame(frame)
btn_frame.pack()

tk.Button(btn_frame, text="Encode", width=12, command=encode_action).pack(side="left", padx=4)
tk.Button(btn_frame, text="Decode", width=12, command=decode_action).pack(side="left", padx=4)
tk.Button(btn_frame, text="Load from File", width=15, command=load_from_file).pack(side="left", padx=4)
tk.Button(btn_frame, text="Save Output", width=12, command=save_to_file).pack(side="left", padx=4)

tk.Label(frame, text="Output:").pack(anchor="w", pady=(10, 0))
output = scrolledtext.ScrolledText(frame, height=8, width=80)
output.pack(fill="x", expand=True)

root.mainloop()