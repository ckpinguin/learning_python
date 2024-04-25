from turtle import Screen
from paddle import Paddle
from ball import Ball
from brick import Brick
from scoreboard import Scoreboard
from message import Message
import time
import random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BALL_SIZE = 20
PADDLE_TORQUE = 20
DEFAULT_GAME_SPEED = 0.02
GAME_ACCELERATION = 1.05
NUM_BRICK_ROWS = 1
NUM_BRICKS_PER_ROW = 1
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_SPACING = 10


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
msg = Message()
msg.write_message()


all_bricks = []

keys_pressed = set()


def get_random_color():
    return random.choice(["red", "green", "blue", "yellow",
                          "orange", "purple", "white", "pink",
                          "cyan", "magenta"])


def setup_bricks():
    for row in range(NUM_BRICK_ROWS):
        print("Row: ", row)
        row_y = 200 - row * (BRICK_HEIGHT + BRICK_SPACING)

        for col in range(NUM_BRICKS_PER_ROW):
            print("Col: ", col)
            col_x = -250 + (BRICK_WIDTH + BRICK_SPACING) * col

            brick = Brick(width=BRICK_WIDTH,
                          height=BRICK_HEIGHT,
                          x=col_x,
                          y=row_y,
                          color=get_random_color(), shape="square")
            all_bricks.append(brick)


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


def detect_side_wall_collision() -> bool:
    return abs(ball.xcor()) >= x_wall


def detect_top_wall_collision() -> bool:
    return ball.ycor() >= y_wall


def detect_bottom_wall_collision() -> bool:
    return ball.ycor() <= -SCREEN_HEIGHT / 2


def detect_brick_collision() -> Brick | None:
    ball_x, ball_y = ball.position()
    for brick in all_bricks:
        brick_x, brick_y = brick.position()
        brick_width = brick.width
        brick_height = brick.height
        margin = 10

        if (
            brick_x - brick_width / 2 <= ball_x <= brick_x + brick_width / 2 + margin  # noqa
            and brick_y - brick_height / 2 <= ball_y <= brick_y + brick_height / 2 + margin  # noqa
        ):
            print("Brick collision detected")
            print("ball_x: ", ball_x, "ball_y: ", ball_y)
            print("brick_x: ", brick_x)
            return brick
    return None

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
    global game_is_running
    for action in keys_pressed:
        actions[action]()

    screen.update()

    if detect_top_wall_collision():
        print("Bouncing off top wall")
        ball.bounce_off_x_walls()

    brick: Brick | None = detect_brick_collision()
    if brick:
        print("Bouncing off brick")
        scoreboard.inc_score()
        scoreboard.write_board()
        ball.bounce_off_x_walls()
        print("Removing brick")
        all_bricks.remove(brick)
        print("Bricks left: ", len(all_bricks))
        brick.hideturtle()
        if len(all_bricks) == 0:
            msg.write_message("You win!", "green")
            screen.update()
            game_is_running = False
            time.sleep(2)  # Pause for 2 seconds before exiting

    if detect_side_wall_collision():
        print("Bouncing off side wall")
        ball.bounce_off_y_walls()

    if detect_paddle_collision(paddle):
        print("Bouncing off paddle")
        game_speed *= 1 / GAME_ACCELERATION
        ball.bounce_off_paddle(paddle.get_torque_offset())

    if detect_bottom_wall_collision():
        print("Hitting bottom wall => you lose!")
        print("len(all_bricks): ", len(all_bricks))
        scoreboard.dec_lives()
        if scoreboard.lives == 0:
            msg.write_message("You lose!", "red")
            screen.update()
            game_is_running = False
            time.sleep(2)
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

setup_bricks()

while game_is_running:
    tick()
screen.exitonclick()
