import pygame
from ship import Ship
from alien import Alien
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, ENEMY_SPEED, CHARACTER_SIZE, BULLET_SIZE, NAV_THICKNESS, ALIEN_ROWS
from bullet import Bullet
from display import Display


class World:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.player = pygame.sprite.GroupSingle()
        self.aliens = pygame.sprite.Group()
        self.display = Display(self.screen)
        self.game_over = False
        self.player_score = 0
        self.game_level = 1
        self._generate_world()

    def _generate_aliens(self):
        alien_cols = (SCREEN_WIDTH // CHARACTER_SIZE) // 2
        alien_rows = ALIEN_ROWS
        for y in range(alien_rows):
            for x in range(alien_cols):
                alien_x = CHARACTER_SIZE * x
                alien_y = CHARACTER_SIZE * y
                specific_pos = (alien_x, alien_y)
                self.aliens.add(Alien(specific_pos, CHARACTER_SIZE, y))

    def _generate_player(self):
        player_x, player_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - CHARACTER_SIZE
        center_size = CHARACTER_SIZE // 2
        player_pos = (player_x - center_size, player_y)
        self.player.add(Ship(player_pos, CHARACTER_SIZE))

    def _generate_world(self):
        self._generate_player()
        self._generate_aliens()

    def player_move(self):
        print("moving player")

    def update(self):
        print("updating world")
