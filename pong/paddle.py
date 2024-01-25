from turtle import Turtle


class Paddle(Turtle):

    STEP_SIZE = 10

    def __init__(self, width=20, height=100, x_pos=350, y_pos=0, min_y=-300, max_y=300):
        super().__init__()
        self.min_y = min_y
        self.max_y = max_y
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=1, stretch_len=5)
        self.width = width
        self.height = height
        self.speed('fastest')
        self.penup()
        self.goto(x_pos, y_pos)
        self.pendown()
        self.last_move = None

    def set_pos(self, x, y):
        self.position(x, y)

    def move_up(self):
        if self.ycor() <= self.max_y:
            self.penup()
            self.clear()
            new_y = self.ycor() + self.STEP_SIZE
            self.sety(new_y)
            self.last_move = "Up"

    def move_down(self):
        if self.ycor() >= self.min_y:
            self.penup()
            self.clear()
            new_y = self.ycor() - self.STEP_SIZE
            self.sety(new_y)
            self.last_move = "Down"
