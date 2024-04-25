from turtle import Turtle


class Paddle(Turtle):

    STEP_SIZE = 10

    def __init__(self, width=200, height=20, x_pos=150, y_pos=-200, min_x=-100, max_x=100):  # noqa
        super().__init__()
        self.min_x = min_x
        self.max_x = max_x
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

    def move_left(self):
        if self.xcor() <= self.max_x:
            self.penup()
            self.clear()
            new_x = self.xcor() - self.STEP_SIZE
            self.setx(new_x)
            self.last_move = "Left"

    def move_right(self):
        if self.xcor() >= self.min_x:
            self.penup()
            self.clear()
            new_x = self.xcor() + self.STEP_SIZE
            self.setx(new_x)
            self.last_move = "Right"