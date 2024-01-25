from turtle import Turtle, Screen
import random

tt = Turtle()

colors = ["pale turquoise", "firebrick",
          "light sky blue", "dim gray", "olive", "yellow green", "navajo white", "dark orchid", "hot pink", "peru", "forest green"]

tt.shape("turtle")
tt.width(5)
tt.speed(5000)

ongoing = True
while ongoing:
    random_color = random.choice(colors)
    tt.color(random_color)
    random_angle = random.randint(0, 360)
    tt.right(random_angle)
    tt.forward(30)

screen = Screen()
screen.exitonclick()
