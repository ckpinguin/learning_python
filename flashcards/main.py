from tkinter import Tk, PhotoImage, Canvas, Button, messagebox
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT = "Arial"
WORDS_FILE = "data/french_words.csv"
TO_LEARN_FILE = "words_to_learn.csv"
LANGUAGE_FROM = "French"
LANGUAGE_TO = "English"
TIME_PER_CARD_MS = 3000

words: list[dict] = []
current_card = []
current_side = "front"


def setup():
    global words
    try:
        print("OK: Learn file found")
        df = pandas.read_csv(TO_LEARN_FILE)

    except FileNotFoundError:
        print("INFO: No learn file found, creating a new one...")
        df = pandas.read_csv(WORDS_FILE)
        df.to_csv(TO_LEARN_FILE, index=False)
    except pandas.errors.EmptyDataError:
        empty_message_and_quit()

    words = df.to_dict(orient="records")
    display_new_card()


def answer_wrong():
    display_new_card()


def answer_correct():
    global current_card
    remove_card(current_card)
    display_new_card()


def display_new_card():
    global current_side, current_card, flip_timer
    window.after_cancel(flip_timer)
    if current_side == "back":
        flip_card("front")
    current_card = get_random_card(words)
    print(f"Current card: {current_card}")
    title = get_card_title(current_card, "front")
    word = current_card[title]
    set_card_text(title, word)
    set_text_color("black")
    canvas.itemconfig(card_bg_id, image=card_front_img)

    flip_timer = window.after(TIME_PER_CARD_MS, toggle_side)
    current_side = "front"


def get_card_title(card: dict, side):
    keys = list(card.keys())
    if side == "front":
        title = keys[0]
    elif side == "back":
        title = keys[1]
    return title


def remove_card(card_to_remove):
    global words
    print(f"Removing {card_to_remove}...")
    words.remove(card_to_remove)
    df = pandas.DataFrame(words)
    df.to_csv(TO_LEARN_FILE, index=False)


def get_random_card(words_dicts):
    try:
        entry = random.choice(words_dicts)
    except IndexError:
        empty_message_and_quit()

    return entry


def empty_message_and_quit():
    print("Great! No more cards to learn!")
    ok = messagebox.askokcancel(
        title="Empty!", message="Great! No more cards to learn!")
    if ok:
        exit(0)


def toggle_side():
    global current_side
    if current_side == "front":
        flip_card("back")
        current_side = "back"
        right_button.config(state="active")
        wrong_button.config(state="active")
    elif current_side == "back":
        flip_card("front")
        current_side = "front"
        right_button.config(state="disabled")
        wrong_button.config(state="disabled")


def flip_card(to_side):
    if to_side == "back":
        canvas.itemconfig(card_bg_id, image=card_back_img)
        title = get_card_title(current_card, "back")
        word = current_card[title]
        set_card_text(title, word)
        set_text_color("white")


def set_card_text(title, word):
    set_title(title)
    set_word(word)


def set_text_color(color):
    canvas.itemconfig(title_id, fill=color)
    canvas.itemconfig(word_id, fill=color)


def set_title(title):
    set_canvas_text(title_id, title)


def set_word(word):
    set_canvas_text(word_id, word)


def set_canvas_text(id, text):
    canvas.itemconfig(id, text=text)


# ##### UI ######
window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(TIME_PER_CARD_MS, toggle_side)

card_back_img = PhotoImage(file="images/card_back.png")
card_front_img = PhotoImage(file="images/card_front.png")
canvas = Canvas(width=800, height=526,
                bg=BACKGROUND_COLOR, highlightthickness=0)
card_bg_id = canvas.create_image(400, 263, image=card_front_img)
title_id = canvas.create_text(400, 150, text="Title", fill="black",
                              font=(FONT, 40, "italic"))

word_id = canvas.create_text(400, 263, text="Word", fill="black",
                             font=(FONT, 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(
    command=answer_wrong,
    state="disabled",
    image=wrong_img, highlightthickness=0, border=0,  bg=BACKGROUND_COLOR)
wrong_button.grid(row=1, column=0)

right_img = PhotoImage(file="images/right.png")
right_button = Button(
    command=answer_correct,
    state="disabled",
    image=right_img, highlightthickness=0,
    border=0,
    bg=BACKGROUND_COLOR)
right_button.grid(row=1, column=1)

setup()
window.mainloop()
