from turtle import Turtle


class ScoreBoard(Turtle):

    FONT = ("Courier", 22, "normal")
    ALIGNMENT = "center"

    def __init__(self, screen_height):
        super().__init__()
        self.score = 0
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, (screen_height / 2) - 30)
        self.write(f"Score: {self.score}",
                   align=self.ALIGNMENT, font=self.FONT)

    def show_score_on_screen(self):
        self.clear()
        self.write(f"Score: {self.score}",
                   align=self.ALIGNMENT, font=self.FONT)

    def update_score(self, new_score):
        self.score = new_score

    def increment_score(self, amount):
        self.score += amount

    def game_over(self):
        self.goto(0, 0)
        self.write("G A M E   O V E R", align=self.ALIGNMENT, font=self.FONT)
