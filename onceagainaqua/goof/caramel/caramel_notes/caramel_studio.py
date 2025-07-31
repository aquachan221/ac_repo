import tkinter as tk
from tkinter import filedialog, scrolledtext
import sys
import io

from parser_lexer import tokenize, Parser, evaluate, Context

class CaramelStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Caramel Studio 🍯")
        self.ctx = Context()

        self.text = tk.Text(root, wrap="none", font=("Consolas", 12), bg="#111", fg="#eee", insertbackground="#eee")
        self.text.pack(fill="both", expand=True)

        self.output = scrolledtext.ScrolledText(root, height=8, state="disabled", bg="#222", fg="#99f", insertbackground="#fff")
        self.output.pack(fill="x", padx=4, pady=(0, 6))

        self.create_buttons()

        self.filename = None

    def create_buttons(self):
        btn_frame = tk.Frame(self.root, bg="#1a1a1a")
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="🗂 Open", command=self.load_file).pack(side="left", padx=4, pady=4)
        tk.Button(btn_frame, text="💾 Save", command=self.save_file).pack(side="left", padx=4)
        tk.Button(btn_frame, text="▶ Run", command=self.run_code).pack(side="right", padx=4)

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Caramel Files", "*.cml"), ("All Files", "*.*")])
        if path:
            with open(path, "r") as f:
                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, f.read())
            self.filename = path
            self.log(f"📂 Loaded {path}")

    def save_file(self):
        if not self.filename:
            self.filename = filedialog.asksaveasfilename(defaultextension=".cml", filetypes=[("Caramel Files", "*.cml")])
        if self.filename:
            with open(self.filename, "w") as f:
                f.write(self.text.get("1.0", tk.END))
            self.log(f"💾 Saved {self.filename}")

    def run_code(self):
        code = self.text.get("1.0", tk.END)
        self.ctx = Context()  # reset context each run
        try:
            tokens = tokenize(code)
            parser = Parser(tokens)
            program = parser.parse_all()
            self.capture_output(lambda: [evaluate(stmt, self.ctx) for stmt in program])
        except Exception as e:
            self.log(f"❌ Error: {e}")

    def capture_output(self, func):
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            func()
            output = sys.stdout.getvalue()
            self.log(output.strip())
        finally:
            sys.stdout = old_stdout

    def log(self, message):
        self.output.config(state="normal")
        self.output.insert(tk.END, message + "\n")
        self.output.see(tk.END)
        self.output.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = CaramelStudio(root)
    root.geometry("800x600")
    root.mainloop()