from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):
    def __init__(self, start_position):
        super().__init__()
        self.shape("turtle")
        self.color("black")
        self.shapesize(stretch_wid=1, stretch_len=1)
        self.penup()
        self.start_x, self.start_y = start_position
        self.start_y += 20
        self.setheading(90)
        self.reset_position()

    def move(self):
        self.clear()
        self.forward(MOVE_DISTANCE)

    def flat(self):
        self.shapesize(stretch_wid=2, stretch_len=2)

    def reset_position(self):
        self.clear()
        self.goto(self.start_x, self.start_y)
