from turtle import Turtle

t = Turtle()
screen = t.getscreen()

step_size = 10
turn_degrees = 10


def forward():
    t.forward(step_size)


def backward():
    t.backward(step_size)


def turn_left():
    new_heading = t.heading() + turn_degrees
    t.setheading(new_heading)


def turn_right():
    new_heading = t.heading() - turn_degrees
    t.setheading(new_heading)


def clear():
    t.clear()
    t.penup()
    t.home()
    t.pendown()


screen.listen()
screen.onkey(forward, "Up")
screen.onkey(forward, "v")

screen.onkey(turn_left, "Left")
screen.onkey(turn_left, "u")

screen.onkey(turn_right, "Right")
screen.onkey(turn_right, "a")

screen.onkey(backward, "Down")
screen.onkey(backward, "i")

screen.onkey(clear, "Escape")

screen.mainloop()
