from turtle import Screen
import time
from snake import Snake
from food import Food
from scoreboard import ScoreBoard

screen_width = 700
screen_height = 700


screen = Screen()
screen.setup(width=screen_width, height=screen_height)
screen.title("Sssssnake!")
screen.bgcolor("black")
screen.tracer(0)

keys_pressed = set()


def end_game():
    global game_is_on
    global food
    screen.resetscreen()
    score_board.reset()
    snake.reset()
    food = Food()
    # game_is_on = False


def tick():
    global game_is_on
    for action in keys_pressed:
        actions[action]()

    time.sleep(0.1)
    snake.move()
    screen.update()

    if is_at_border(snake):
        end_game()
    if snake.detect_self_collision():
        end_game()
    if snake.head.distance(food) < 15:
        score_board.increase_score(1)
        score_board.show_score_on_screen()
        food.new_random_pos()
        snake.extend()


actions = dict(
    up=lambda: snake.move_up(),
    left=lambda: snake.move_left(),
    right=lambda: snake.move_right(),
    down=lambda: snake.move_down()
)


def is_at_border(snake: Snake):
    x_pos, y_pos = snake.head_position()
    if x_pos >= screen_width / 2 or x_pos <= -(screen_width / 2) + 20:
        return True
    if y_pos >= screen_height / 2 or y_pos <= -(screen_height / 2) + 20:
        return True
    return False


snake = Snake()
food = Food()
score_board = ScoreBoard(screen_height)

screen.onkeypress(lambda: keys_pressed.add("up"), "Up")
screen.onkeyrelease(lambda: keys_pressed.remove("up"), "Up")
screen.onkeypress(lambda: keys_pressed.add("left"), "Left")
screen.onkeyrelease(lambda: keys_pressed.remove("left"), "Left")
screen.onkeypress(lambda: keys_pressed.add("right"), "Right")
screen.onkeyrelease(lambda: keys_pressed.remove("right"), "Right")
screen.onkeypress(lambda: keys_pressed.add("down"), "Down")
screen.onkeyrelease(lambda: keys_pressed.remove("down"), "Down")
screen.listen()


# screen.onkey(clear, "Escape")

game_is_on = True
while game_is_on:
    tick()


screen.exitonclick()
