from turtle import Turtle


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.score = 0
        self.lives = 3
        self.write_board()

    def inc_score(self, amount=1):
        self.score += amount

    def dec_lives(self):
        self.lives -= 1

    def write_board(self):
        self.clear()
        self.goto(-50, 250)
        self.write(f"Score: {self.score}   Lives: {self.lives}", align="center",
                   font=("Courier", 20, "normal"))
        self.goto(0, 200)
