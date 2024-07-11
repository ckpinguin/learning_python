import tkinter as tk
from tkinter import ttk  # themed tk


class WriterUI(tk.Tk):
    def __init__(self, timeout: float = 5):
        super().__init__()
        self.title("Dangerous Writing App")
        self.geometry("800x600")

        self.score = 0
        self.timeout = timeout
        self.timer_value = timeout
        self.timer_running = False

        self.create_widgets()

    def create_widgets(self):
        # Frame for the score
        self.score_frame = ttk.Frame(self, padding="10")
        self.score_frame.pack(fill=tk.X)

        self.score_label = ttk.Label(
            self.score_frame, text="Score:", font=("Arial", 16))
        self.score_label.pack(side=tk.LEFT)

        self.score_value = ttk.Label(
            self.score_frame, text=f"{self.score}", font=("Arial", 16))
        self.score_value.pack(side=tk.LEFT, padx=10)

        # Timer label in the score frame
        self.timer_value_label = ttk.Label(
            self.score_frame, text=f"{self.timer_value:.1f}",
            font=("Arial", 14))
        self.timer_value_label.pack(side=tk.RIGHT, padx=10)

        self.timer_label = ttk.Label(
            self.score_frame, text="Timer:", font=("Arial", 14))
        self.timer_label.pack(side=tk.RIGHT)

        # Frame for the text area
        self.text_frame = ttk.Frame(self, padding="10")
        self.text_frame.pack(fill=tk.BOTH, expand=True)

        self.text_area = tk.Text(
            self.text_frame, wrap=tk.WORD, font=("Arial", 14))
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.text_area.bind("<Key>", self.on_key_press)

        # Create a tag for fading effect
        self.text_area.tag_configure("fade", foreground="black")

        # Button to reset the game
        self.reset_button = ttk.Button(
            self, text="Reset Game", command=self.reset_game)
        self.reset_button.pack(pady=10)

    def update_timer(self):
        if self.timer_running:
            self.timer_value -= 0.1
            self.timer_value_label.config(text=f"{self.timer_value:.1f}")
            if self.timer_value > 0.1:
                self.after(100, self.update_timer)
                self.fade_text()
            else:
                self.clear_text_area()

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    def on_key_press(self, event):
        self.restart_timer()
        self.update_score()

    def update_score(self):
        self.score = len(self.text_area.get("1.0", tk.END))
        self.score_value.config(text=f"{self.score}")

    def restart_timer(self, event=None):
        self.timer_value = self.timeout
        self.timer_value_label.config(text=f"{self.timer_value:.1f}")
        if not self.timer_running:  # on first keypress
            self.start_timer()

    def fade_text(self):
        fade_step = 255 / (self.timeout * 10)
        color_value = min(255, int(fade_step *
                          (self.timeout * 10 - self.timer_value * 10)))
        color_hex = f"#{color_value:02x}{color_value:02x}{color_value:02x}"
        self.text_area.tag_configure("fade", foreground=color_hex)
        self.text_area.tag_add("fade", "1.0", tk.END)
        self.after(100, self.fade_text)

    def clear_text_area(self):
        self.text_area.delete("1.0", tk.END)
        self.stop_timer()

    def reset_game(self):
        self.timer_value = self.timeout
        self.timer_value_label.config(text=f"{self.timer_value:.1f}")
        self.score = 0
        self.score_value.config(text=f"{self.score}")
        self.clear_text_area()
