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


# This feels like it belongs to a class...
def is_at_border(snake):
    x_pos, y_pos = snake.head_position()
    if x_pos >= screen_width / 2 or x_pos <= -(screen_width / 2) + 20:
        print("Boing x")
        return True
    if y_pos >= screen_height / 2 or y_pos <= -(screen_height / 2) + 20:
        print("Boing y")
        return True
    return False


snake = Snake()
food = Food()
score_board = ScoreBoard(screen_height)

screen.listen()
screen.onkey(snake.move_up, "Up")
screen.onkey(snake.move_up, "v")

screen.onkey(snake.move_left, "Left")
screen.onkey(snake.move_left, "u")

screen.onkey(snake.move_right, "Right")
screen.onkey(snake.move_right, "a")

screen.onkey(snake.move_down, "Down")
screen.onkey(snake.move_down, "i")

# screen.onkey(clear, "Escape")

game_is_on = True
while game_is_on:
    snake.move()
    time.sleep(0.1)
    screen.update()

    if is_at_border(snake):
        # snake.turn_around()
        score_board.game_over()
        game_is_on = False
    # snake.print_all_segments_pos()
    if snake.detect_self_collision():
        score_board.game_over()
        game_is_on = False
    if snake.head.distance(food) < 15:
        score_board.increment_score(1)
        score_board.show_score_on_screen()
        food.new_random_pos()
        snake.extend()


screen.exitonclick()
