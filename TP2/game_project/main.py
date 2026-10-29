import sys
import pygame

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)    # Player Color
RED = (255, 50, 50)      # Monster Color
YELLOW = (255, 255, 0)   # Bullet Color


class Bullet:
    """Represents a projectile shot by the Player."""

    def __init__(self, x: int, y: int):
        self.width = 6
        self.height = 14
        self.rect = pygame.Rect(x - self.width // 2, y, self.width, self.height)
        self.speed = 8
        self.is_active = True

    def update(self):
        """Move projectile upward and deactivate when off-screen."""
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.is_active = False

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, YELLOW, self.rect)


class Player:
    """Represents the player controlled by arrow keys/WASD and Spacebar to shoot."""

    def __init__(self, x: int, y: int):
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 5
        self.cooldown = 0  # Cooldown timer to control shooting rate

    def handle_input(self, bullets: list):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # Keep player within screen bounds
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Handle shooting with Spacebar
        if self.cooldown > 0:
            self.cooldown -= 1
        if keys[pygame.K_SPACE] and self.cooldown == 0:
            bullets.append(Bullet(self.rect.centerx, self.rect.top))
            self.cooldown = 15  # Frame delay between shots

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, BLUE, self.rect)


class Monster:
    """Represents an enemy patrolling horizontally."""

    def __init__(self, x: int, y: int, width: int = 40, height: int = 40, speed_x: int = 3):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed_x = speed_x
        self.is_alive = True

    def update(self, screen_width: int):
        """Patrol across screen boundaries."""
        if not self.is_alive:
            return
        self.rect.x += self.speed_x
        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.speed_x *= -1

    def draw(self, surface: pygame.Surface):
        if self.is_alive:
            pygame.draw.rect(surface, RED, self.rect)


class GameBoard:
    """Encapsulates the Pygame window, game loop, entities, and collision logic."""

    def __init__(self, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("M1 GSI - 2D Game OOP (Homework)")
        self.clock = pygame.time.Clock()
        self.running = True

        # Instantiate Game Elements
        self.player = Player(x=380, y=500)
        self.monster = Monster(x=200, y=100)
        self.bullets = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.player.handle_input(self.bullets)

    def update(self):
        # Update monster movement
        self.monster.update(self.width)

        # Update active bullets and check collisions
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_active:
                self.bullets.remove(bullet)
                continue

            # Check collision between Bullet and Monster
            if self.monster.is_alive and bullet.rect.colliderect(self.monster.rect):
                self.monster.is_alive = False
                bullet.is_active = False
                if bullet in self.bullets:
                    self.bullets.remove(bullet)

    def draw(self):
        self.screen.fill(BLACK)
        self.player.draw(self.screen)
        self.monster.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    board = GameBoard()
    board.run()