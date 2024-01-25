from turtle import Turtle
from typing import List


class Snake():
    STARTING_POSITIONS = [(-20, 0), (-40, 0)]
    MOVE_DISTANCE = 20

    DIRECTIONS = {
        "RIGHT": 0,
        "UP": 90,
        "LEFT": 180,
        "DOWN": 270
    }
    #   UP = 90
    #   LEFT = 180
    #   DOWN = 270

    def __init__(self):
        super().__init__()
        self.segments: List[Turtle] = []
        self.head = None
        self._setup_snake()

    def reset(self):
        for segment in self.segments:
            segment.clear()
            del segment
        self.segments.clear()
        self._setup_snake()

    def _setup_snake(self):
        self._setup_head()
        for position in Snake.STARTING_POSITIONS:
            self._add_segment(position)
        self.head = self.segments[0]

    def _setup_head(self):
        head = Turtle("square")
        head.color("green")
        head.penup()
        head.goto(0, 0)
        self.segments.append(head)

    def move(self):
        self._segments_follow_head()
        self.head.forward(self.MOVE_DISTANCE)

    def _segments_follow_head(self):
        for seg_num in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[seg_num-1].xcor()
            new_y = self.segments[seg_num-1].ycor()
            segment = self.segments[seg_num]
            segment.goto(new_x, new_y)

    # Normally not allowed:
    def _turn_around(self):
        self.head.right(180)

    def extend(self):
        position = self.segments[-1].position()
        self._add_segment(position)

    def _add_segment(self, position):
        new_segment = Turtle("square")
        new_segment.color("white")
        new_segment.penup()
        new_segment.goto(position)
        self.segments.append(new_segment)

    def detect_self_collision(self):
        for segment in self.segments[1:]:
            if segment == self.head:
                pass
            if self.head.distance(segment) < 10:
                return True
        return False

    def move_up(self):
        if self._is_turn_allowed(self.DIRECTIONS["UP"]):
            self.head.setheading(self.DIRECTIONS["UP"])

    def move_down(self):
        if self._is_turn_allowed(self.DIRECTIONS["DOWN"]):
            self.head.setheading(self.DIRECTIONS["DOWN"])

    def move_right(self):
        if self._is_turn_allowed(self.DIRECTIONS["RIGHT"]):
            self.head.setheading(self.DIRECTIONS["RIGHT"])

    def move_left(self):
        if self._is_turn_allowed(self.DIRECTIONS["LEFT"]):
            self.head.setheading(self.DIRECTIONS["LEFT"])

    def _is_turn_allowed(self, new_direction):
        current_direction = self.head.heading()
        if (abs(new_direction - current_direction)) == 180:
            return False
        return True

    def head_position(self):
        return self.segments[0].pos()

    def print_all_segments_pos(self):
        print("All segments")
        for seg in self.segments:
            print(seg.pos())
        print("############")
