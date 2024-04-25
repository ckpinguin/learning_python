from turtle import Screen
from paddle import Paddle
from ball import Ball
from brick import Brick
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

# print(f"y_wall: {y_wall}, x_wall: {x_wall}")
screen = Screen()
screen.bgcolor("black")
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.tracer(0)
screen.title("Breakout!")
screen.mode("logo")

paddle = Paddle(torque=PADDLE_TORQUE)
ball = Ball(size=BALL_SIZE, x=0, y=-220)
scoreboard = Scoreboard()
brick1 = Brick(width=100, height=30, x=-250,
               y=100, color="red", shape="square")

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


def detect_side_wall_collision():
    return abs(ball.xcor()) >= x_wall


def detect_brick_collision():
    print
    return False


def detect_top_wall_collision():
    return ball.ycor() >= y_wall


def detect_bottom_wall_collision():
    return ball.ycor() <= -SCREEN_HEIGHT / 2

# Since the paddle is rectangular, we need to check for collision on both
# the x and y axis, the distance method alone is not sufficient


def detect_paddle_collision(paddle: Paddle):
    ball_x, ball_y = ball.position()
    paddle_x, paddle_y = paddle.position()
    paddle_width = paddle.width
    paddle_height = paddle.height
    margin = 10

    if (
        paddle_x - paddle_width / 2 <= ball_x <= paddle_x + paddle_width / 2 + margin  # noqa
        and paddle_y - paddle_height / 2 <= ball_y <= paddle_y + paddle_height / 2 + margin  # noqa
    ):
        print("Paddle collision detected")
        print("ball_x: ", ball_x, "ball_y: ", ball_y)
        print("paddle_x: ", paddle_x)
        return True
    else:
        return False


def reset_field_after_loss():
    global game_speed
    scoreboard.write_board()
    game_speed = DEFAULT_GAME_SPEED
    ball.reset_to_start()
    paddle.reset_to_start()
    screen.update()
    time.sleep(1)


def tick():
    global game_speed
    for action in keys_pressed:
        actions[action]()

    screen.update()

    if detect_top_wall_collision():
        print("Bouncing off top wall")
        ball.bounce_off_x_walls()
        # ball.bounce()

    if detect_brick_collision():
        print("Bouncing off brick")
        scoreboard.inc_score()
        ball.bounce_off_x_walls()

    if detect_side_wall_collision():
        print("Bouncing off side wall")
        ball.bounce_off_y_walls()

    if detect_paddle_collision(paddle):
        print("Bouncing off paddle")
        game_speed *= 1 / GAME_ACCELERATION
        ball.bounce_off_paddle(paddle.get_torque_offset())

    if detect_bottom_wall_collision():
        print("Hitting bottom wall => you lose!")
        reset_field_after_loss()

    ball.move()
    time.sleep(game_speed)


actions = dict(
    left=lambda: paddle.move_left(),
    right=lambda: paddle.move_right(),

)

screen.onkeypress(lambda: keys_pressed.add("left"), key="Left")
screen.onkeyrelease(lambda: keys_pressed.remove("left"), key="Left")
screen.onkeypress(lambda: keys_pressed.add("right"), key="Right")
screen.onkeyrelease(lambda: keys_pressed.remove("right"), key="Right")

screen.onkeyrelease(pause_game, "p")

screen.listen()

pause = False
game_is_running = True

while game_is_running:
    tick()
screen.exitonclick()
