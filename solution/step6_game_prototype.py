import sys
import pygame

# Initialize Pygame
pygame.init()

# Game Window Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Color Definitions (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)   # Player Color
RED = (255, 50, 50)     # Monster Color

class Player:
    def __init__(self, x, y):
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 5

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # Keep player within screen boundaries
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)


class Monster:
    def __init__(self, x, y):
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed_x = 3

    def update(self):
        # Patrol horizontally across the screen
        self.rect.x += self.speed_x
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.speed_x *= -1  # Reverse direction at boundaries

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("M1 GSI - 2D Game Prototype")
    clock = pygame.time.Clock()

    # Instantiate Player and Monster
    player = Player(x=100, y=300)
    monster = Monster(x=600, y=300)

    # Main Game Loop
    running = True
    while running:
        # 1. Input Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.handle_input()

        # 2. Object Updates
        monster.update()

        # 3. Rendering / Drawing
        screen.fill(BLACK)
        player.draw(screen)
        monster.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()