from tkinter import Tk, Label, Canvas, PhotoImage, Button
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
CHECKMARK = "✔️"


timer = None
reps = 0


def start_timer():
    global reps
    reps += 1

    timer_work = WORK_MIN * 60
    timer_short_break = SHORT_BREAK_MIN * 60
    timer_long_break = LONG_BREAK_MIN * 60

    start_button.config(state="disabled")
    window.attributes('-topmost', 0)
    if reps == 8:
        count_down(timer_long_break)
        status_label.config(text="Long Break", fg=RED)
        window.attributes('-topmost', 1)
        window.attributes('-fullscreen', True)
    elif reps % 2 == 0:
        count_down(timer_short_break)
        status_label.config(text="Short Break", fg=PINK)
        window.attributes('-topmost', 1)
        window.attributes('-fullscreen', True)
    else:
        count_down(timer_work)
        status_label.config(text="Work", fg=GREEN)
        status_label.config(text="Work", fg=GREEN)
        window.attributes('-topmost', 0)
        window.attributes('-fullscreen', False)


def reset_timer():
    global reps
    window.after_cancel(timer)
    status_label.config(text="")
    checkmarks_label.config(text="")
    canvas.itemconfig(timer_text, text="")
    start_button.config(state="normal")
    window.attributes('-topmost', 0)
    window.attributes('-fullscreen', False)
    reps = 0


def count_down(count):
    global timer
    minutes, seconds = divmod(count, 60)
    text = f"{minutes:02}:{seconds:02}"
    canvas.itemconfig(timer_text, text=text)
    if count > 0:
        timer = window.after(1000, count_down, count-1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✓"
        checkmarks_label.config(text=marks)


window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

status_label = Label(text="", width=12,  fg=GREEN,
                     bg=YELLOW, font=(FONT_NAME, 48))
status_label.grid(row=0, column=1)

tomato_img = PhotoImage(file="tomato.png")
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(
    100, 130, text="", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

start_button = Button(text="Start", bg=YELLOW,
                      highlightbackground=YELLOW, highlightthickness=0, command=start_timer)
start_button.grid(row=2, column=0)


reset_button = Button(text="Reset", bg=YELLOW,
                      highlightbackground=YELLOW, highlightthickness=0, command=reset_timer)
reset_button.grid(row=2, column=2)

checkmarks_label = Label(text="", font=(
    FONT_NAME, 32, "bold"), bg=YELLOW, fg=GREEN)
checkmarks_label.grid(row=3, column=1)

window.mainloop()
