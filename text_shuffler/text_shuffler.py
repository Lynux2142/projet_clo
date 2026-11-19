import random
import tkinter as tk
from tkinter import ttk

def shuffle_text(text: str) -> str:
    lines = text.split("\n")
    result_lines = []

    for line in lines:
        letters = [c for c in line if c.isalpha()]
        random.shuffle(letters)

        result_line = list(line)
        letter_index = 0
        for j, c in enumerate(result_line):
            if c.isalpha():
                result_line[j] = letters[letter_index]
                letter_index += 1

        result_lines.append("".join(result_line))

    return "\n".join(result_lines)


class TextShufflerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Text Shuffler")
        self.root.geometry("600x600")

        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        label = ttk.Label(main_frame, text="Enter text to shuffle:")
        label.pack(anchor=tk.W, pady=(0, 5))

        pane = ttk.PanedWindow(main_frame, orient=tk.VERTICAL)
        pane.pack(fill=tk.BOTH, expand=True, pady=5)

        input_frame = ttk.Frame(pane)
        self.input_text = tk.Text(input_frame, wrap=tk.WORD, font=("Arial", 11))
        input_scroll = ttk.Scrollbar(input_frame, orient=tk.VERTICAL, command=self.input_text.yview)
        self.input_text.configure(yscrollcommand=input_scroll.set)

        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        input_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        pane.add(input_frame, weight=1)

        output_frame = ttk.Frame(pane)
        self.output_text = tk.Text(output_frame, wrap=tk.WORD, font=("Arial", 11))
        output_scroll = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=output_scroll.set)

        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        output_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        pane.add(output_frame, weight=1)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        shuffle_button = ttk.Button(btn_frame, text="Shuffle Text", command=self.on_shuffle)
        shuffle_button.pack(side=tk.LEFT, padx=(0, 8))

    def on_shuffle(self):
        content = self.input_text.get("1.0", tk.END).rstrip("\n")

        shuffled = shuffle_text(content)

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", shuffled)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextShufflerApp(root)
    root.mainloop()
