from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

SCREEN_WIDTH = 600
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
screen.title("Breakout!")
screen.mode("logo")

paddle = Paddle()
ball = Ball()
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


def detect_x_wall_collision():
    return abs(ball.xcor()) >= x_wall


def detect_paddle_collision(paddle):
    return ball.distance(paddle) <= 50 \
        and abs(ball.xcor()) > x_wall - 40


def get_paddle_torque_offset(paddle: Paddle):
    if paddle.last_move == "Left":
        return -PADDLE_TORQUE
    else:
        return +PADDLE_TORQUE


def reset_field_after_score():
    scoreboard.write_board()
    global game_speed
    game_speed = DEFAULT_GAME_SPEED
    ball.reset_to_start()


def tick():
    global game_speed
    for action in keys_pressed:
        actions[action]()
    screen.update()
    if detect_x_wall_collision():
        ball.bounce_off_y_walls()
        # ball.bounce()
    if detect_paddle_collision(paddle):
        game_speed *= 1 / GAME_ACCELERATION
        ball.bounce_off_paddle(get_paddle_torque_offset(paddle))

    if ball.ycor() > y_wall - 10:
        scoreboard.inc_l_score()
        reset_field_after_score()
    if ball.ycor() < -y_wall + 10:
        scoreboard.inc_r_score()
        reset_field_after_score()

    ball.move()
    time.sleep(game_speed)


actions = dict(
    left=lambda: paddle.move_left(),
    right=lambda: paddle.move_right(),

)

screen.onkeypress(lambda: keys_pressed.add("left"), key="Left")
screen.onkeypress(lambda: keys_pressed.add("right"), key="Right")

screen.onkeyrelease(pause_game, "p")

screen.listen()

pause = False
game_is_running = True

while game_is_running:
    tick()
screen.exitonclick()
