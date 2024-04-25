from turtle import Turtle


class Message(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.write_message()

    def write_message(self, msg="", color="white"):
        self.color(color)
        print("message.py: Writing message")
        self.clear()
        self.goto(-50, 0)
        self.write(msg, align="center",
                   font=("Courier", 60, "normal"))
