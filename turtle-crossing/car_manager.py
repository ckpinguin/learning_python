from turtle import Turtle
import random
from typing import List

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager():
    def __init__(self, screen_width=600, screen_height=600):
        self.upper_boundary = screen_height / 2 - 50
        self.lower_boundary = -screen_height / 2 + 50
        self.left_boundary = -screen_width / 2
        self.right_boundary = screen_width / 2
        self.starting_point = self.right_boundary
        self.cars: List[CarManager.Car] = []
        self.random_create_chance = 10  # 1 in _10_

    def move_all_cars(self):
        for car in self.cars:
            car.move()
            if car.xcor() <= self.left_boundary:
                car.reset()
                car.hideturtle()
                self.cars.remove(car)
                del car

    def check_collision(self, obj: Turtle):
        for car in self.cars:
            if obj.distance(car) < 20:
                return True
        return False

    def put_random_car(self):
        n = random.randint(0, 100)
        if n % self.random_create_chance == 0:
            self.create_random_car()

    def create_random_car(self):
        color = random.choice(COLORS)
        pos_x = self.starting_point
        pos_y = random.randint(self.lower_boundary, self.upper_boundary)
        car = CarManager.Car(color)
        car.setpos(pos_x, pos_y)
        self.cars.append(car)

    class Car(Turtle):
        def __init__(self, color):
            super().__init__()
            self.penup()
            self.color(color)
            # self.hideturtle()
            self.shape("square")
            self.shapesize(stretch_wid=1, stretch_len=2)
            self.setheading(180)
            self.move_speed = random.randint(4, MOVE_INCREMENT)

        def move(self):
            self.clear()
            self.forward(self.move_speed)
