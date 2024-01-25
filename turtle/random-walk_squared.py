from turtle import Turtle, Screen
import random

tt = Turtle()

colors = ["pale turquoise", "firebrick",
          "light sky blue", "dim gray", "olive", "yellow green", "navajo white", "dark orchid", "hot pink", "peru", "forest green"]
headings = [90, 180, 270, 360]

tt.shape("turtle")
tt.width(5)
tt.speed(5000)

ongoing = True
while ongoing:
    random_color = random.choice(colors)
    tt.color(random_color)
    random_heading = random.choice(headings)
    tt.setheading(random_heading)
    tt.forward(30)

screen = Screen()
screen.exitonclick()
