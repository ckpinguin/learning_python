from tkinter import Tk, Label, Canvas, PhotoImage, Button
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"
FONT_NAME = "Arial"


class WriterInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.score_label = Label(
            text=f"Score: {self.quiz.score}", width=12,
            fg="white", bg=THEME_COLOR, font=(FONT_NAME, 16))
        self.score_label.grid(row=0, column=1)

        self.canvas = Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(
            150, 125,
            text="Question example",
            fill=THEME_COLOR, font=(FONT_NAME, 20, "italic")
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        self.false_image = PhotoImage(file="images/false.png")
        self.true_image = PhotoImage(file="images/true.png")
        self.false_button = Button(image=self.false_image,
                                   highlightbackground=THEME_COLOR,
                                   highlightthickness=0,
                                   command=lambda: self.check_answer("False"))
        self.true_button = Button(
            image=self.true_image,
            highlightbackground=THEME_COLOR,
            highlightthickness=0,
            command=lambda: self.check_answer("True"))
        self.false_button.grid(
            row=2, column=0)
        self.true_button.grid(
            row=2, column=1)

        self.get_next_question()

        self.window.mainloop()

    # Violation of SRP, but we leave this method here for reference
    # The UI should not „get“ or „check“ something outside
    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            current_question = self.quiz.next_question()
            formatted_question = self.get_formatted_text(current_question)
            self.canvas.itemconfig(self.question_text, text=formatted_question)
        else:
            self.canvas.itemconfig(
                self.question_text, text="You have reached the\nend of the quiz!")
            self.false_button.config(state="disabled")
            self.true_button.config(state="disabled")

    # Violation of SRP, but we leave this method here for reference
    def check_answer(self, answer: str):
        if self.quiz.check_answer(answer) is True:
            self.flash_green()
        else:
            self.flash_red()
        self.score_label.config(text=f"Score: {self.quiz.score}")

    def flash_red(self):
        self.canvas.config(bg="red")
        self.window.after(1000, self.get_next_question)

    def flash_green(self):
        self.canvas.config(bg="green")
        self.window.after(1000, self.get_next_question)

    def get_formatted_text(self, input_text: str):
        line_length = 25  # You can adjust this value based on your needs
        lines = [input_text[i:i + line_length]
                 for i in range(0, len(input_text), line_length)]

        # Join the lines with newline characters
        formatted_text = '\n'.join(lines)
        return formatted_text
