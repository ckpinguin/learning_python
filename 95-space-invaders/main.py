import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, NAV_THICKNESS
from world import World

pygame.init()
# display surface
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Invaders Clone Attack')


class Main:
    def __init__(self, screen):
        self.screen = screen
        self.FPS = pygame.time.Clock()

    def main(self):
        world = World(self.screen)
        while True:
            self.screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("Fire!")
                        world.player_move(attack=True)
            world.player_move()
            world.update()
            pygame.display.update()
            self.FPS.tick(60)


if __name__ == "__main__":
    play = Main(screen)
    play.main()
