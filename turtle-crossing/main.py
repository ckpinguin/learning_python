import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

DEFAULT_GAME_SPEED = 0.1
GAME_ACCELERATION = 1.05
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

screen = Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.tracer(0)
screen.title("Turtler")
screen.bgcolor("white")

scoreboard = Scoreboard((-SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
car_manager = CarManager(SCREEN_WIDTH)
player = Player(start_position=(0, -SCREEN_HEIGHT/2))

keys_pressed = set()
game_speed = DEFAULT_GAME_SPEED


def tick():
    global game_speed
    global game_is_on
    for action in keys_pressed:
        actions[action]()
    scoreboard.display_level()
    car_manager.put_random_car()
    car_manager.move_all_cars()
    if check_goal_reached(player, SCREEN_HEIGHT/2):
        scoreboard.incLevel()
        game_speed = increase_speed(game_speed)
        player.reset_position()
    if car_manager.check_collision(player):
        player.flat()
        game_is_on = False
        scoreboard.game_over()

    screen.update()
    time.sleep(game_speed)


def increase_speed(speed):
    return speed * 1 / GAME_ACCELERATION


def check_goal_reached(player: Player, goal: int):
    return player.ycor() >= goal


actions = dict(
    up=lambda: player.move()
)

screen.onkeypress(lambda: keys_pressed.add("up"), key="Up")
screen.onkeyrelease(lambda: keys_pressed.remove("up"), key="Up")
screen.listen()

game_is_on = True
while game_is_on:
    tick()

screen.exitonclick()
