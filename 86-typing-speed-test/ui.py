from tkinter import Tk, Entry, Label, Button, END
from TypingSpeedTest import TypingSpeedTest
from time import time


THEME_COLOR = "#375362"
FONT_NAME = "Arial"


class TypingSpeedTestUI(Tk):
    def __init__(self, ts_test: TypingSpeedTest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ts_test = ts_test
        self.running = True
        self.start_time = None
        self.end_time = None

        self.typing_speed_wpm = 0
        self.typing_speed_cpm = 0
        self.words_typed = 0
        self.characters_typed = 0

        self.title("Typing Speed Tester")
        self.config(padx=20, pady=20, bg=THEME_COLOR)

        self.label_score = Label(
            text=f"Score: {self.ts_test.score}", width=12,
            fg="white", bg=THEME_COLOR, font=(FONT_NAME, 16))
        self.label_score.grid(row=0, column=1)

        random_sentence = self.ts_test.create_random_sentence()
        self.text_sentence = Label(
            self, fg="black", bg="white", text=random_sentence,
            font=(FONT_NAME, 14), width=100, height=10
        )
        self.text_sentence.grid(row=1, columnspan=3)

        self.label_entry_field = Label(
            self, bg=THEME_COLOR, fg="white",
            font=(FONT_NAME, 14),
            text="Type the sentences here, a word is counted on pressing of Spacebar")  # noqa
        self.label_entry_field.grid(row=2, columnspan=3)

        self.entry = Entry(font=(FONT_NAME, 24))
        self.entry.grid(row=3, columnspan=3)

        self.btn_exit = Button(self, text="Quit", command=self.stop_game)
        self.btn_exit.grid(row=0, column=2)

        self.result_label = Label(self, font=(FONT_NAME, 18))
        self.result_label.grid(row=0, column=0)

        self.bind("<KeyPress>", self.on_key_pressed)
        self.bind("<KeyRelease>", self.on_key_released)
        self.bind("<space>", (lambda e: self.on_finish_word()))
        self.bind("<Return>", (lambda e: self.on_finish_word()))

    def on_key_pressed(self, event):
        if event.char == ".":
            print("Finished sentence.")
            self.on_finish_sentence()
        if self.start_time is None:
            self.start_time = time()
            print("Timer started!")

    def on_key_released(self, event):
        if self.start_time is not None and self.end_time is not None:
            self.end_time = time()
            self.calculate_typing_speed()

    def on_finish_word(self):
        answer = self.entry.get()
        print(f"Processing word: {answer}")
        self.words_typed += 1
        self.characters_typed += len(answer)
        print(f"Words typed so far: {self.words_typed}")
        print(f"Characters typed so far: {self.characters_typed}")
        self.calculate_typing_speed()
        self.display_typing_speed()
        self.entry.delete(0, END)

    def on_finish_sentence(self):
        self.on_finish_word()

    def calculate_typing_speed(self):
        # Calculate typing speed in words per minute (WPM) and
        # types per minute (TPM)
        if self.start_time is not None and self.end_time is not None:
            elapsed_time = self.end_time - self.start_time
            self.typing_speed_wpm = int((self.words_typed / elapsed_time) * 60)
            self.typing_speed_cpm = int(
                (self.characters_typed / elapsed_time) * 60)

    def stop_game(self):
        self.running = False
        self.destroy()

    def display_typing_speed(self):
        # Display the typing speed result
        result_text = f"Your typing speed: {
            self.typing_speed_wpm} WPM and {self.typing_speed_cpm} CPM"
        self.result_label.config(text=result_text)
        # Stop the application after displaying the result
        # self.stop_game()
