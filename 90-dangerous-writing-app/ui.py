import tkinter as tk
from tkinter import ttk


class SimpleUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple UI")
        self.root.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        # Frame for the score
        self.score_frame = ttk.Frame(self.root, padding="10")
        self.score_frame.pack(fill=tk.X)

        self.score_label = ttk.Label(
            self.score_frame, text="Score:", font=("Arial", 14))
        self.score_label.pack(side=tk.LEFT)

        self.score_value = ttk.Label(
            self.score_frame, text="0", font=("Arial", 14))
        self.score_value.pack(side=tk.LEFT, padx=10)

        # Frame for the text area
        self.text_frame = ttk.Frame(self.root, padding="10")
        self.text_frame.pack(fill=tk.BOTH, expand=True)

        self.text_area = tk.Text(
            self.text_frame, wrap=tk.WORD, font=("Arial", 12))
        self.text_area.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleUI(root)
    root.mainloop()
