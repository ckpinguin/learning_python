import turtle
import pandas

# Howto get coords for the input file:
""" def get_mouse_click_coor(x, y):
        print(x, y)
    turtle.onscreenclick(get_mouse_click_coor) """

screen = turtle.Screen()
screen.title("U.S. States game")


FONT = ("Arial", 16, "normal")
image = "./blank_states_img.gif"
screen.addshape(image)
# background = turtle.Turtle()
# background.shape(image)
# Simpler than using a turtle shape as background:
screen.bgpic(image)

state_writer = turtle.Turtle()
state_writer.penup()
state_writer.hideturtle()

df = pandas.read_csv('50_states.csv')
all_states = df.state.to_list()
guessed_states = []

while len(guessed_states) < df.state.size:
    answer_state = screen.textinput(
        title=f"{len(guessed_states)}/{df.state.size}", prompt="What's another state's name? (Type Exit to stop)").title()

    if answer_state == "Exit":
        missing_states = [
            state for state in all_states if state not in guessed_states]
        df = pandas.DataFrame(missing_states)
        df.to_csv("states_to_learn.csv")
        break

    if answer_state in all_states:
        guessed_states.append(answer_state)
        state_data = df[df.state == answer_state]
        state_writer.goto(int(state_data.x), int(state_data.y))
        state_writer.write(state_data.state.item(), align="center", font=FONT)


turtle.mainloop()
