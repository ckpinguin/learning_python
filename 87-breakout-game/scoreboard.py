from turtle import Turtle


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.score = 0
        self.write_board()

    def inc_score(self, amount=1):
        self.score += amount

    def write_board(self):
        self.clear()
        self.goto(-100, 200)
        self.write(self.score, align="center",
                   font=("Courier", 80, "normal"))
        self.goto(0, 200)
