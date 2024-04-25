from turtle import Turtle


class Brick(Turtle):

    def __init__(self, width=100, height=30, x=-250, y=100, color="red", shape="square"):  # noqa
        super().__init__()
        self.x_pos = x
        self.y_pos = y
        self.shape(shape)
        self.color(color)
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.width = width
        self.height = height
        self.penup()
        self.goto(self.x_pos, self.y_pos)
        self.pendown()

    def set_pos(self, x, y):
        self.position(x, y)
