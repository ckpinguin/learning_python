from turtle import Turtle


class Paddle(Turtle):

    STEP_SIZE = 10

    def __init__(self, torque=20, width=100, height=20, x_pos=0, y_pos=-250, min_x=-250, max_x=250):  # noqa
        super().__init__()
        self.min_x = min_x
        self.max_x = max_x
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.width = width
        self.height = height
        self.speed('fastest')
        self.penup()
        self.goto(x_pos, y_pos)
        self.pendown()
        self.last_move = None
        self.torque = torque
        self.start_x = x_pos
        self.start_y = y_pos

    def set_pos(self, x, y):
        self.position(x, y)

    def move_left(self):
        if self.xcor() >= self.min_x:
            self.penup()
            self.clear()
            new_x = self.xcor() - self.STEP_SIZE
            self.setx(new_x)
            self.last_move = "Left"

    def move_right(self):
        if self.xcor() <= self.max_x:
            self.penup()
            self.clear()
            new_x = self.xcor() + self.STEP_SIZE
            self.setx(new_x)
            self.last_move = "Right"

    def get_torque_offset(self):
        if self.last_move == "Left":
            return -self.torque
        elif self.last_move == "Right":
            return +self.torque
        else:
            return 0

    def reset_to_start(self):
        self.penup()
        self.clear()
        self.goto(self.start_x, self.start_y)
        self.pendown()
