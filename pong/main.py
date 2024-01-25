from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_SIZE = 20
PADDLE_TORQUE = 20
DEFAULT_GAME_SPEED = 0.02
GAME_ACCELERATION = 1.05


y_wall = SCREEN_HEIGHT / 2 - BALL_SIZE
x_wall = SCREEN_WIDTH / 2 - BALL_SIZE

game_speed = DEFAULT_GAME_SPEED

print(f"y_wall: {y_wall}, x_wall: {x_wall}")
screen = Screen()
screen.bgcolor("black")
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.tracer(0)
screen.title("Pong!")
screen.mode("logo")

right_paddle = Paddle()
left_paddle = Paddle(x_pos=-350)
ball = Ball(initial_angle=random.randint(10, 350))
scoreboard = Scoreboard()

keys_pressed = set()


def pause_game():
    """
    Toggle the pause state.
    """
    global pause
    if not pause:
        pause = True
        pause_loop()
    else:
        pause = False


def pause_loop():
    """
    Do nothing while in pause.
    """
    while pause:
        time.sleep(game_speed)
        screen.update()


def detect_y_wall_collision():
    return abs(ball.ycor()) >= y_wall


def detect_paddle_collision(paddle):
    return ball.distance(paddle) <= 50 \
        and abs(ball.xcor()) > x_wall - 40


def get_paddle_torque_offset(paddle):
    if paddle.last_move == "Up":
        return -PADDLE_TORQUE
    else:
        return +PADDLE_TORQUE


def reset_field_after_score():
    scoreboard.write_board()
    global game_speed
    game_speed = DEFAULT_GAME_SPEED
    ball.reset_to_start(random.randint(10, 350))


def tick():
    global game_speed
    for action in keys_pressed:
        actions[action]()
    screen.update()
    if detect_y_wall_collision():
        ball.bounce_off_y_walls()
        # ball.bounce()
    if detect_paddle_collision(left_paddle):
        game_speed *= 1 / GAME_ACCELERATION
        ball.bounce_off_paddle(get_paddle_torque_offset(left_paddle))
    if detect_paddle_collision(right_paddle):
        game_speed *= 1 / GAME_ACCELERATION
        ball.bounce_off_paddle(get_paddle_torque_offset(right_paddle))

    if ball.xcor() > x_wall - 10:
        scoreboard.inc_l_score()
        reset_field_after_score()
    if ball.xcor() < -x_wall + 10:
        scoreboard.inc_r_score()
        reset_field_after_score()

    ball.move()
    time.sleep(game_speed)


actions = dict(
    up_right=lambda: right_paddle.move_up(),
    down_right=lambda: right_paddle.move_down(),
    up_left=lambda: left_paddle.move_up(),
    down_left=lambda: left_paddle.move_down()
)

screen.onkeypress(lambda: keys_pressed.add("up_right"), key="Up")
screen.onkeypress(lambda: keys_pressed.add("down_right"), key="Down")
screen.onkeyrelease(lambda: keys_pressed.remove("up_right"), key="Up")
screen.onkeyrelease(lambda: keys_pressed.remove("down_right"), key="Down")
screen.onkeypress(lambda: keys_pressed.add("up_left"), key="v")
screen.onkeypress(lambda: keys_pressed.add("down_left"), key="i")
screen.onkeyrelease(lambda: keys_pressed.remove("up_left"), key="v")
screen.onkeyrelease(lambda: keys_pressed.remove("down_left"), key="i")

screen.onkeyrelease(pause_game, "p")

screen.listen()

pause = False
game_is_running = True

while game_is_running:
    tick()
screen.exitonclick()
