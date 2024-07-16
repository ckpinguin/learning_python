import pygame
from ship import Ship
from alien import Alien
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, ENEMY_SPEED, CHARACTER_SIZE, BULLET_SIZE, NAV_THICKNESS
from bullet import Bullet
from display import Display


class World:
    def __init__(self, screen):
        self.screen = screen
        self.player = pygame.sprite.GroupSingle()
        self.player = pygame.sprite.Group()
        self.display = Display(self.screen)
        self.game_over = False
        self.player_score = 0
        self.game_level = 1
        self._generate_world()

    def _generate_world(self):
        print("generating world")

    def player_move(self):
        print("moving player")

    def update(self):
        print("updating world")
