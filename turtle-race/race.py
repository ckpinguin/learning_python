from turtle import Turtle, Screen
import random

colors = ['blue', 'green', 'chocolate', 'black', 'red', 'pink']
race_distance = 700
screen_height = len(colors) * 58
bottom = -(screen_height/2)
start_line = -(race_distance/2)+25
finishing_line = (race_distance/2)-30
stepAmount = 10
turtles = []


class RunningTurtle(Turtle):
    def __init__(self, name="__Nobody"):
        super().__init__()
        self.shape("turtle")
        # self.shape("turtle")
        self.name = name
        self.penup()

    def get_color(self):
        return self.color()[0]

    def is_owned_by(self, name):
        return self.name == name


def get_random_color(colors):
    return random.choice(colors)


def draw_line(xPos, yPos, length):
    t = Turtle()
    t.width(5)
    t.penup()
    t.setposition(xPos, yPos)
    t.right(90)
    t.pendown()
    stepSize = int(length/10)
    for i in range(0, 10):
        if i % 2 == 0:
            t.color("white")
        else:
            t.color("black")
        t.forward(stepSize)
    t.hideturtle()


screen = Screen()
screen.setup(width=race_distance, height=screen_height)

# draw_line(finishing_line, 300, 300)
yOffset = bottom
for color in colors:
    yOffset += 50
    turtle = RunningTurtle()
    turtle.color(color)
    turtle.setposition(x=start_line, y=yOffset)
    turtles.append(turtle)


user_bet_color = screen.textinput(
    "Bet on a turtle!", f"Who will win this race? {colors}: ")
user_name = screen.textinput(
    "Turtle name", "What's the name of your turtle?: "
)
for turtle in turtles:
    if turtle.get_color() == user_bet_color:
        turtle.name = user_name


racing = True
while racing:
    for turtle in turtles:
        if turtle.is_owned_by(user_name):
            turtle.clear()
            turtle.write(user_name, align="right", font=("Arial", 16, "bold"))
        turtle.forward(random.randint(0, 10))
        if turtle.pos()[0] >= finishing_line:
            # turtle.shapesize(5)
            racing = False

# After the race
for turtle in turtles:
    if turtle.is_owned_by(user_name):
        turtle.clear()
        if turtle.pos()[0] >= finishing_line:
            turtle.write("YOU WIN!", align="right",
                         font=("Arial", 18, "bold"))
        else:
            turtle.write("YOU LOSE!", align="right",
                         font=("Arial", 18, "bold"))

screen.exitonclick()
