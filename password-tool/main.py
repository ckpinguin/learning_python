from tkinter import (Tk, PhotoImage, messagebox,
                     Canvas, Label, Entry, Button, StringVar, END)
import random
import pyperclip
import json

PASSWORD_FILE = "passwords.json"
DEFAULT_EMAIL = "ck@pm.me"
FONT_NAME = "Arial"
DEFAULT_FONT = (FONT_NAME, 10, "normal")
DEFAULT_MSG = ""
MESSAGE_TIMEOUT_MS = 5000


PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#0a6522"
YELLOW = "#f7f5dd"
BLACK = "#000000"
WHITE = "#ffffff"

# ---------------- PASSWORD GENERATOR --------------- #


def generate_password():
    chars = "abcdefghijklmnopqrstuvwxyz"
    numbers = "0123456789"
    symbols = "!#$%&()*+"
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    pw_letters = [random.choice(chars) for _ in range(nr_letters)]
    pw_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    pw_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    pw_list = pw_letters + pw_numbers + pw_symbols
    shuffled_pw = shuffle_list(pw_list)
    clear_password_entry()
    password_entry.insert(0, string=shuffled_pw)
    pyperclip.copy(shuffled_pw)


def shuffle_list(char_list):
    random.shuffle(char_list)
    shuffled_string = ''.join(char_list)
    return shuffled_string


def clear_password_entry():
    content = password_entry.get()
    if content:
        password_entry.delete(0, END)


# ------------------ SAVE PASSWORD ------------------ #

def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {
        website:   {
            "email": username,
            "password": password,
        }
    }

    if website and username and password:
        is_ok = messagebox.askokcancel(
            title=website, message=f"These are the details entered:\nEmail: {username}\nPassword: {password} \n\nIs it OK to save?")
        if is_ok:
            try:
                with open(PASSWORD_FILE, "r") as file:
                    data: dict = json.load(file)
                    # Not just appending, we need a valid json structure
                    data.update(new_data)
            except FileNotFoundError:
                write_json(new_data)
            else:
                write_json(data)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                info_msg("Password saved.")

    else:
        alert_msg("Not all fields\n are filled.")


def write_json(data):
    with open(PASSWORD_FILE, "w") as file:
        json.dump(data, file, indent=4)


def search_password(identifier):
    try:
        with open(PASSWORD_FILE, "r") as file:
            data = json.load(file)
            update_loaded_fields(data[identifier])

    except FileNotFoundError:
        alert_msg("No password file found.\nPlease add some passwords first.")
    except KeyError:
        alert_msg(f"No password found for {identifier}.")
    finally:
        pyperclip.copy(password_entry.get())


def update_loaded_fields(record):
    username_entry.delete(0, END)
    username_entry.insert(0, record["email"])
    password_entry.delete(0, END)
    password_entry.insert(0, record["password"])
# ------------------ UI SETUP --------------------- #


def reset_msg():
    message_label.config(text=DEFAULT_MSG, fg=BLACK, font=DEFAULT_FONT)


def alert_msg(text, timeout=MESSAGE_TIMEOUT_MS):
    message_label.config(text=text,
                         fg=RED, font=(FONT_NAME, 12, "bold"))
    message_label.after(timeout, reset_msg)


def info_msg(text, timeout=MESSAGE_TIMEOUT_MS):
    message_label.config(text=text,
                         fg=GREEN, font=(FONT_NAME, 12, "normal"))
    message_label.after(timeout, reset_msg)


window = Tk()
window.title("Password Manager")
window.config(heigh=220, padx=20, pady=20)


# Row 0
message_label = Label(text=DEFAULT_MSG, font=DEFAULT_FONT)
message_label.grid(row=0, column=0, columnspan=3)

# Row 1
mypass_img = PhotoImage(file="logo.png")
canvas = Canvas(height=200, width=200, highlightthickness=0)
canvas.create_image(100, 100, image=mypass_img)
# timer_text = canvas.create_text(
#    100, 130, text="", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)


# Row 2
website_label = Label(text="Website:", font=DEFAULT_FONT)
website_label.grid(row=2, column=0)
website = StringVar()
website_entry = Entry(width=35, textvariable=website, font=DEFAULT_FONT)
website_entry.grid(row=2, column=1, columnspan=1, sticky="EW")

search_button = Button(text="Search", highlightthickness=0, font=DEFAULT_FONT,
                       command=lambda: search_password(website_entry.get()))
search_button.grid(row=2, column=2, sticky="EW")
window.bind('<Return>', lambda event: search_password(website_entry.get()))


# Row 3
username_label = Label(text="Email/Username:", font=DEFAULT_FONT)
username_label.grid(row=3, column=0)
username = StringVar()
username_entry = Entry(width=35, textvariable=username, font=DEFAULT_FONT)
username_entry.insert(0, DEFAULT_EMAIL)
username_entry.grid(row=3, column=1, columnspan=2, sticky="EW")


# Row 4
password_label = Label(text="Password:", font=DEFAULT_FONT)
password_label.grid(row=4, column=0)
password = StringVar()
password_entry = Entry(width=21, textvariable=password, font=DEFAULT_FONT)
password_entry.grid(row=4, column=1)
password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(row=4, column=2, sticky="EW")


# Row 5
add_button = Button(text="Add", width=36,
                    highlightthickness=0, command=save_password, font=DEFAULT_FONT)
add_button.grid(row=5, column=1, columnspan=2, sticky="EW")


window.mainloop()
