import turtle as t
import random

tt = t.Turtle()
t.colormode(255)

tt.shape("turtle")
tt.width(1)
tt.speed(20)


radius = 100
circle_offset = 5
turn = 10
move_length = 50


def draw_circles(radius, offset):
    for _ in range(int(360 / offset)):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        tt.color((r, g, b))
        tt.circle(radius)
        tt.right(circle_offset)


def move_circle_start(turn, amount):
    tt.right(turn)
    tt.forward(amount)


ongoing = True
while ongoing:
    draw_circles(radius, circle_offset)
    move_circle_start(turn, move_length)

screen = t.Screen()
screen.exitonclick()
