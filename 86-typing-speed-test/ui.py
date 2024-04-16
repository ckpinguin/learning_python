from tkinter import Tk, Entry, Label, Button, END
from TypingSpeedTest import TypingSpeedTest
from time import time


THEME_COLOR = "#375362"
FONT_NAME = "Arial"


class TypingSpeedTestUI(Tk):
    def __init__(
            self, ts: TypingSpeedTest, game_time=60, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ts = ts

        self.game_time = game_time
        self.remaining_game_time = self.game_time

        self.running = False
        self.start_type_time = None
        self.end_type_time = None

        # UI elements
        self.title("Typing Speed Tester")
        self.config(padx=20, pady=20, bg=THEME_COLOR)

        self.label_result = Label(
            self, text="Press Start to begin the test!",
            bg=THEME_COLOR, fg="white", font=(FONT_NAME, 16))
        self.label_result.grid(row=0, column=0)

        self.label_timer = Label(
            self, text=f"Time left: {self.remaining_game_time}", font=(FONT_NAME, 12))  # noqa
        self.label_timer.grid(row=0, column=1)

        self.btn_start_stop = Button(
            self, text="Start", command=self.start_game)
        self.btn_start_stop.grid(row=0, column=2)

        self.btn_exit = Button(self, text="Quit", command=self.quit_game)
        self.btn_exit.grid(row=0, column=3)

        self.label_sentence = Label(
            self, fg="black", bg="white", text="As soon as the game starts, type the words appearing in here into the text field below...",  # noqa
            font=(FONT_NAME, 14), width=100, height=10
        )
        self.label_sentence.grid(row=1, columnspan=4)

        self.label_entry_field = Label(
            self, bg=THEME_COLOR, fg="white",
            font=(FONT_NAME, 14),
            text="Type the sentences here, a word is counted on pressing of Spacebar")  # noqa
        self.label_entry_field.grid(row=2, columnspan=4)

        self.field_entry = Entry(self, font=(FONT_NAME, 24))
        self.field_entry.grid(row=3, columnspan=4)

    def start_game(self):
        self.ts.reset_stats()
        self.ts.set_new_random_sentence()
        self.label_sentence.config(text=self.ts.sentence)
        self.remaining_game_time = self.game_time
        self.running = True
        self.btn_start_stop.config(text="Stop", command=self.stop_game)
        self.field_entry.config(state="normal")
        self.field_entry.delete(0, END)
        self.field_entry.focus_set()
        self.bind_event_handlers()
        self.start_game_timer()

    def bind_event_handlers(self):
        self.bind("<KeyPress>", self.on_key_pressed)
        self.bind("<KeyRelease>", self.on_key_released)
        self.bind("<space>", (lambda e: self.on_finish_word()))
        self.bind("<Return>", (lambda e: self.on_finish_word()))

    def start_game_timer(self):
        # Schedule the function to stop the game after the specified time
        self.after(self.game_time * 1000, self.stop_game)
        self.update_timer()

    def stop_game(self):
        self.running = False
        self.btn_start_stop.config(text="Start", command=self.start_game)
        self.unbind_event_handlers()
        self.field_entry.config(state="disabled")

    def unbind_event_handlers(self):
        self.unbind("<KeyPress>")
        self.unbind("<KeyRelease>")
        self.unbind("<space>")
        self.unbind("<Return>")

    def quit_game(self):
        self.running = False
        self.destroy()

    def update_timer(self):
        self.remaining_game_time -= 1
        self.label_timer.config(
            text=f"Time left: {self.remaining_game_time} secs")
        if self.remaining_game_time > 0:
            self.after(1000, self.update_timer)
        else:
            self.stop_game()

    def display_typing_speed(self):
        # Display the typing speed result
        result_text = f"Your average typing speed: {
            self.ts.typing_speed_wpm} WPM and {self.ts.typing_speed_cpm} CPM"
        self.label_result.config(text=result_text)

    # Event handlers

    def on_key_pressed(self, event):
        if event.char == ".":
            print("Finished sentence.")
            self.on_finish_sentence()
        if self.start_type_time is None:
            self.start_type_time = time()
            self.end_type_time = self.start_type_time
            print("Timer started!")

    def on_key_released(self, event):
        if self.start_type_time is not None and self.end_type_time is not None:
            self.end_type_time = time()

    def on_finish_word(self):
        answer = self.field_entry.get()

        if self.ts.check_word_in_sentence(answer):
            self.ts.update_stats(answer)
            self.ts.remove_word_from_sentence(answer)
            if self.ts.is_sentence_finished():
                self.ts.set_new_random_sentence()
            # Only count correct typed words
            self.ts.calculate_typing_speed(
                self.start_type_time, self.end_type_time)
        self.label_sentence.config(text=self.ts.sentence)

        self.display_typing_speed()
        self.field_entry.delete(0, END)

    def on_finish_sentence(self):
        self.on_finish_word()
