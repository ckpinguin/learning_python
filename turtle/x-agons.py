from turtle import Turtle, Screen
import random

tt = Turtle()

colors = ["pale turquoise", "firebrick",
          "light sky blue", "dim gray", "olive", "yellow green", "navajo white", "dark orchid", "hot pink", "peru", "forest green"]

tt.shape("turtle")
tt.width(2)
tt.speed(5)


def draw_shape(num_sides):
    angle = 360 / num_sides

    for _ in range(0, num_sides):
        color = random.choice(colors)
        tt.color(color)
        tt.forward(100)
        tt.right(angle)


for i in range(4, 10):
    draw_shape(i)


screen = Screen()
screen.exitonclick()
