from turtle import Turtle


class Ball(Turtle):

    DEFAULT_SPEED = 5

    def __init__(self, size=20, x=0, y=-220):
        super().__init__()
        self.color("white")
        self.shape("circle")
        self.penup()
        self.setheading(0)
        self.goto(x, y)
        self.pendown()
        self.size = size

    def reset_to_start(self):
        self.penup()
        self.goto(0, -220)
        self.setheading(0)
        self.pendown()

    def move(self, speed=DEFAULT_SPEED):
        self.clear()
        self.forward(speed)

    def bounce_off_paddle(self, offset=0):
        print(f"ball.py: Bouncing off paddle, heading: \{self.heading()}, offset={offset}")
        print(f"new heading: {(self.heading() - 180 + offset) % 360}")
        self.setheading((self.heading() - 180 + offset) % 360)

    def bounce_off_y_walls(self):
        print(f"ball.py: Bouncing off y walls, heading: {self.heading()}")
        print(f"new heading: {360 - self.heading()}")
        self.setheading(360 - self.heading())

    def bounce_off_x_walls(self):
        print(f"ball.py: Bouncing off x walls, heading: {self.heading()}")
        print(f"new heading: {180 - self.heading()}")
        self.setheading(180 - self.heading())
