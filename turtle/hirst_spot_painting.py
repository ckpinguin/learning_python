import turtle as t
import random
import colorgram

tt = t.Turtle()
tt.hideturtle()
tt.penup()
t.colormode(255)
screen = tt.getscreen()

tt.width(1)
tt.speed(50)

colors = colorgram.extract('spot-painting.jpg', 50)
num_colors = len(colors)


num_lines = 10
num_spots_on_line = 10
gap_between_spots = 40
spot_size = 20


def choose_random_color():
    random_idx = random.randint(0, num_colors - 1)
    return colors[random_idx].rgb


def jump_to_next_line():
    current_ypos = tt.pos()[1]
    tt.setpos(0, current_ypos + 30)


screen.setworldcoordinates(0, 500, 500, 0)
tt.setpos(0, 0)
for _ in range(0, num_lines):
    for _ in range(0, num_spots_on_line):
        random_color = choose_random_color()
        tt.pendown()
        tt.begin_fill()
        tt.dot(spot_size, random_color)
        tt.end_fill()
        tt.penup()
        tt.forward(gap_between_spots)
    jump_to_next_line()
