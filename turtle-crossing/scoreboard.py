from turtle import Turtle

FONT_SIZE = 24
FONT = ("Courier", FONT_SIZE, "normal")


class Scoreboard(Turtle):
    def __init__(self, position):
        super().__init__()
        self.pos_x, self.pos_y = position
        self.hideturtle()
        self.penup()
        self.current_level = 0

    def display_level(self):
        self.clear()
        self.goto(self.pos_x + FONT_SIZE, self.pos_y - FONT_SIZE)
        self.write(f"Level: {self.current_level}", font=FONT)

    def game_over(self):
        self.goto(0, 0)
        self.write("G A M E  O V E R", align="center", font=FONT)

    def incLevel(self, inc=1):
        self.current_level += inc
