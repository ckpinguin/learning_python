from turtle import Turtle


class Ball(Turtle):

    DEFAULT_SPEED = 5

    def __init__(self, initial_angle=45):
        super().__init__()
        self.color("white")
        self.shape("circle")
        self.penup()
        self.setheading(initial_angle)

    def reset_to_start(self, angle):
        self.goto(0, 0)
        self.setheading(angle)

    def move(self, speed=DEFAULT_SPEED):
        self.clear()
        self.forward(speed)

    def bounce_off_paddle(self, offset=0):
        self.setheading((-self.heading() + offset) % 360)

    def bounce_off_y_walls(self):
        self.setheading(180 - self.heading())
