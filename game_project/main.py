import math
import os
import sys
from abc import ABC, abstractmethod
import pygame

# Dynamic path resolution to project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

# Colors (RGB)
RED = (220, 50, 50)
GREEN = (50, 220, 80)
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40)
CYAN = (80, 220, 255)
ORANGE = (255, 140, 0)


# ==========================================================
# 1. DIP: Abstract Damage-Calculation Mechanism
# ==========================================================
class DamageCalculator(ABC):
    """Abstract strategy for calculating damage taken by a monster."""

    @abstractmethod
    def calculate_damage(self, weapon_type: str, base_damage: float) -> float:
        pass


class StandardDamageCalculator(DamageCalculator):
    """Normal damage calculation (100% of base damage)."""

    def calculate_damage(self, weapon_type: str, base_damage: float) -> float:
        return base_damage


class WeaponResistantCalculator(DamageCalculator):
    """Reduces damage from a specific weapon type (e.g., 50% resistant to bullets)."""

    def __init__(self, resistant_to: str = "bullet", multiplier: float = 0.5):
        self.resistant_to = resistant_to
        self.multiplier = multiplier

    def calculate_damage(self, weapon_type: str, base_damage: float) -> float:
        if weapon_type == self.resistant_to:
            return base_damage * self.multiplier
        return base_damage


class WeaponWeaknessCalculator(DamageCalculator):
    """Receives bonus damage from a specific weapon type (e.g., +50% damage from bullets)."""

    def __init__(self, weak_to: str = "bullet", multiplier: float = 1.5):
        self.weak_to = weak_to
        self.multiplier = multiplier

    def calculate_damage(self, weapon_type: str, base_damage: float) -> float:
        if weapon_type == self.weak_to:
            return base_damage * self.multiplier
        return base_damage


# ==========================================================
# 2. ISP: Segregated Monster Ability Interfaces
# ==========================================================
class Movable(ABC):
    @abstractmethod
    def move(self, screen_width: int):
        pass


class Flyable(ABC):
    @abstractmethod
    def fly(self, screen_height: int):
        pass


class Shootable(ABC):
    @abstractmethod
    def shoot(self, enemy_bullets: list):
        pass


class Shieldable(ABC):
    @abstractmethod
    def activate_shield(self):
        pass

    @abstractmethod
    def has_active_shield(self) -> bool:
        pass


# ==========================================================
# 3. Projectiles & Player
# ==========================================================
class Bullet:
    """Represents a projectile shot by the Player."""

    def __init__(self, x: int, y: int, weapon_type: str = "bullet", damage: float = 25.0):
        self.width = 20
        self.height = 32
        self.rect = pygame.Rect(x - self.width // 2, y, self.width, self.height)
        self.speed = 8
        self.weapon_type = weapon_type
        self.damage = damage
        self.is_active = True

        # Load bullet sprite
        image_path = os.path.join(ASSETS_DIR, "bulet.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def update(self):
        """Move projectile upward and deactivate when off-screen."""
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.is_active = False

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)


class EnemyBullet:
    """Represents a projectile fired downward by a Shootable monster."""

    def __init__(self, x: int, y: int):
        self.width = 10
        self.height = 20
        self.rect = pygame.Rect(x - self.width // 2, y, self.width, self.height)
        self.speed = 5
        self.is_active = True

    def update(self, screen_height: int):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.is_active = False

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, ORANGE, self.rect, border_radius=4)


class Player:
    """Represents the player controlled by arrow keys/WASD and Spacebar to shoot."""

    def __init__(self, x: int, y: int):
        self.width = 80
        self.height = 80
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 5
        self.cooldown = 0

        # Player health state
        self.label = "Player"
        self.max_health = 100
        self.health = 100
        self.is_alive = True

        # Load player sprite
        image_path = os.path.join(ASSETS_DIR, "player.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        # Load shooting sound effect (.mp3)
        shoot_sound_path = os.path.join(ASSETS_DIR, "shoot.mp3")
        self.shoot_sound = pygame.mixer.Sound(shoot_sound_path)
        self.shoot_sound.set_volume(0.5)

    def take_damage(self, amount: int):
        """Reduce player health when hit by an enemy projectile."""
        if not self.is_alive:
            return
        self.health = max(0, self.health - amount)
        if self.health == 0:
            self.is_alive = False

    def handle_input(self, bullets: list):
        if not self.is_alive:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Handle shooting with Spacebar
        if self.cooldown > 0:
            self.cooldown -= 1
        if keys[pygame.K_SPACE] and self.cooldown == 0:
            bullets.append(Bullet(self.rect.centerx, self.rect.top))
            self.shoot_sound.play()
            self.cooldown = 15

    def draw(self, surface: pygame.Surface):
        if self.is_alive:
            surface.blit(self.image, self.rect)


# ==========================================================
# 4. SRP & LSP: Core Monster Base Class (No Rendering Logic)
# ==========================================================
class Monster:
    """Base enemy class responsible only for state, health, and damage handling."""

    def __init__(
        self,
        x: int,
        y: int,
        label: str = "Monster",
        width: int = 75,
        height: int = 75,
        max_health: float = 100.0,
        damage_calculator: DamageCalculator = None,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.max_health = max_health
        self.health = max_health
        self.is_alive = True
        self.damage_calculator = damage_calculator or StandardDamageCalculator()

    def take_damage(self, weapon_type: str, base_damage: float):
        """Apply damage calculated via the injected DamageCalculator (DIP)."""
        if not self.is_alive:
            return
        final_damage = self.damage_calculator.calculate_damage(weapon_type, base_damage)
        self.health = max(0.0, self.health - final_damage)
        if self.health == 0:
            self.is_alive = False

    def update(self, screen_width: int, screen_height: int, enemy_bullets: list):
        """Polymorphic update hook safe for any Monster subtype (LSP)."""
        pass


# ==========================================================
# 5. OCP, LSP & ISP: Specialized Monster Subtypes
# ==========================================================
class NormalMonster(Monster, Movable):
    """Standard horizontally patrolling monster."""

    def __init__(self, x: int, y: int, speed_x: int = 3):
        super().__init__(
            x=x,
            y=y,
            label="Normal",
            max_health=100.0,
            damage_calculator=StandardDamageCalculator(),
        )
        self.speed_x = speed_x

    def move(self, screen_width: int):
        self.rect.x += self.speed_x
        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.speed_x *= -1

    def update(self, screen_width: int, screen_height: int, enemy_bullets: list):
        if self.is_alive:
            self.move(screen_width)


class FastMonster(Monster, Movable):
    """High-speed patrolling monster, vulnerable to bullets."""

    def __init__(self, x: int, y: int, speed_x: int = 6):
        super().__init__(
            x=x,
            y=y,
            label="Fast",
            max_health=75.0,
            damage_calculator=WeaponWeaknessCalculator(weak_to="bullet", multiplier=1.5),
        )
        self.speed_x = speed_x

    def move(self, screen_width: int):
        self.rect.x += self.speed_x
        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.speed_x *= -1

    def update(self, screen_width: int, screen_height: int, enemy_bullets: list):
        if self.is_alive:
            self.move(screen_width)


class FlyingMonster(Monster, Movable, Flyable):
    """Monster that patrols horizontally and oscillates vertically."""

    def __init__(self, x: int, y: int, speed_x: int = 4):
        super().__init__(
            x=x,
            y=y,
            label="Flying",
            max_health=100.0,
            damage_calculator=StandardDamageCalculator(),
        )
        self.speed_x = speed_x
        self.base_y = y
        self.flight_tick = 0.0

    def move(self, screen_width: int):
        self.rect.x += self.speed_x
        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.speed_x *= -1

    def fly(self, screen_height: int):
        self.flight_tick += 0.08
        new_y = int(self.base_y + math.sin(self.flight_tick) * 35)
        self.rect.y = max(30, min(screen_height // 2, new_y))

    def update(self, screen_width: int, screen_height: int, enemy_bullets: list):
        if self.is_alive:
            self.move(screen_width)
            self.fly(screen_height)


class StrongMonster(Monster, Movable, Shieldable):
    """Armored monster with a shield and 50% resistance to bullets."""

    def __init__(self, x: int, y: int, speed_x: int = 2):
        super().__init__(
            x=x,
            y=y,
            label="Strong",
            max_health=150.0,
            damage_calculator=WeaponResistantCalculator(resistant_to="bullet", multiplier=0.5),
        )
        self.speed_x = speed_x
        self.shield_active = True

    def move(self, screen_width: int):
        self.rect.x += self.speed_x
        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.speed_x *= -1

    def activate_shield(self):
        self.shield_active = self.health > (self.max_health * 0.3)

    def has_active_shield(self) -> bool:
        return self.shield_active

    def update(self, screen_width: int, screen_height: int, enemy_bullets: list):
        if self.is_alive:
            self.activate_shield()
            self.move(screen_width)


class ImmobileMonster(Monster):
    """Stationary monster (does not implement Movable, yet satisfies LSP)."""

    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            label="Immobile",
            max_health=100.0,
            damage_calculator=StandardDamageCalculator(),
        )


class ShooterMonster(Monster, Movable, Shootable):
    """Monster that patrols and periodically fires projectiles downward."""

    def __init__(self, x: int, y: int, speed_x: int = 3):
        super().__init__(
            x=x,
            y=y,
            label="Shooter",
            max_health=100.0,
            damage_calculator=StandardDamageCalculator(),
        )
        self.speed_x = speed_x
        self.shoot_cooldown = 90

    def move(self, screen_width: int):
        self.rect.x += self.speed_x
        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.speed_x *= -1

    def shoot(self, enemy_bullets: list):
        self.shoot_cooldown -= 1
        if self.shoot_cooldown <= 0:
            enemy_bullets.append(EnemyBullet(self.rect.centerx, self.rect.bottom))
            self.shoot_cooldown = 110

    def update(self, screen_width: int, screen_height: int, enemy_bullets: list):
        if self.is_alive:
            self.move(screen_width)
            self.shoot(enemy_bullets)


# ==========================================================
# 6. SRP: Separate Rendering & Health Bar Display Components
# ==========================================================
class MonsterRenderer:
    """Responsible solely for rendering Monster sprites (SRP)."""

    def __init__(self):
        image_path = os.path.join(ASSETS_DIR, "monster.png")
        self.base_image = pygame.image.load(image_path).convert_alpha()

    def draw(self, surface: pygame.Surface, monster: Monster):
        if not monster.is_alive:
            return
        scaled_sprite = pygame.transform.scale(self.base_image, monster.rect.size)
        surface.blit(scaled_sprite, monster.rect)

        # Draw visual shield aura if monster implements Shieldable and shield is active
        if isinstance(monster, Shieldable) and monster.has_active_shield():
            pygame.draw.ellipse(surface, CYAN, monster.rect.inflate(10, 10), width=2)


class HealthBarDisplay:
    """Responsible solely for displaying an entity's health bar and label (SRP)."""

    def __init__(self):
        self.font = pygame.font.SysFont("arial", 13, bold=True)

    def draw(self, surface: pygame.Surface, entity):
        if not entity.is_alive:
            return

        bar_width = entity.rect.width
        bar_height = 7
        bar_x = entity.rect.x
        bar_y = max(18, entity.rect.y - 12)

        # Draw entity label above health bar
        label_surface = self.font.render(entity.label, True, WHITE)
        label_rect = label_surface.get_rect(centerx=entity.rect.centerx, bottom=bar_y - 2)
        surface.blit(label_surface, label_rect)

        # Background bar
        pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))

        # Foreground health bar
        health_ratio = entity.health / entity.max_health if entity.max_health > 0 else 0
        current_width = int(bar_width * health_ratio)
        pygame.draw.rect(surface, GREEN, (bar_x, bar_y, current_width, bar_height))

        # Thin border
        pygame.draw.rect(surface, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height), width=1)


# ==========================================================
# 7. GameBoard Controller
# ==========================================================
class GameBoard:
    """Encapsulates the Pygame window, game loop, entities, audio, and collision logic."""

    def __init__(self, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT):
        pygame.init()
        pygame.mixer.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("M1 GSI - 2D Game OOP (SOLID Monster Refactor)")
        self.clock = pygame.time.Clock()
        self.running = True

        # Load background image
        image_path = os.path.join(ASSETS_DIR, "background.jpg")
        self.background = pygame.image.load(image_path).convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        # Load hit/death sound effect (.mp3)
        die_sound_path = os.path.join(ASSETS_DIR, "die.mp3")
        self.die_sound = pygame.mixer.Sound(die_sound_path)
        self.die_sound.set_volume(0.7)

        # Load and play background music (.mp3)
        music_path = os.path.join(ASSETS_DIR, "music.mp3")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1)

        # Rendering components (SRP)
        self.monster_renderer = MonsterRenderer()
        self.health_bar_display = HealthBarDisplay()

        # Initialize game entities
        self.player: Player = None
        self.monsters: list[Monster] = []
        self.bullets: list[Bullet] = []
        self.enemy_bullets: list[EnemyBullet] = []
        self.reset_game()

    def reset_game(self):
        """Initialize or reset player, monsters, and projectiles."""
        self.player = Player(x=460, y=490)
        self.monsters = [
            ImmobileMonster(x=460, y=35),
            NormalMonster(x=120, y=95),
            FastMonster(x=680, y=155),
            FlyingMonster(x=320, y=120),
            StrongMonster(x=760, y=60),
            ShooterMonster(x=200, y=200),
        ]
        self.bullets.clear()
        self.enemy_bullets.clear()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and not self.player.is_alive:
                    self.reset_game()

        self.player.handle_input(self.bullets)

    def update(self):
        if not self.player.is_alive:
            return

        # Update all monsters polymorphically (LSP)
        for monster in self.monsters:
            monster.update(self.width, self.height, self.enemy_bullets)

        # Update player bullets and check collisions with monsters
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_active:
                self.bullets.remove(bullet)
                continue

            for monster in self.monsters:
                if monster.is_alive and bullet.rect.colliderect(monster.rect):
                    monster.take_damage(bullet.weapon_type, bullet.damage)
                    bullet.is_active = False
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if not monster.is_alive:
                        self.die_sound.play()
                    break

        # Update enemy bullets and check collisions with Player
        for e_bullet in self.enemy_bullets[:]:
            e_bullet.update(self.height)
            if not e_bullet.is_active:
                self.enemy_bullets.remove(e_bullet)
            elif self.player.is_alive and e_bullet.rect.colliderect(self.player.rect):
                self.player.take_damage(20)
                self.enemy_bullets.remove(e_bullet)
                if not self.player.is_alive:
                    self.die_sound.play()

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Draw player and player health bar
        self.player.draw(self.screen)
        self.health_bar_display.draw(self.screen, self.player)

        # Draw monsters and their health bars
        for monster in self.monsters:
            self.monster_renderer.draw(self.screen, monster)
            self.health_bar_display.draw(self.screen, monster)

        # Draw player and enemy projectiles
        for bullet in self.bullets:
            bullet.draw(self.screen)

        for e_bullet in self.enemy_bullets:
            e_bullet.draw(self.screen)

        # Display Game Over overlay if player health reaches 0
        if not self.player.is_alive:
            font = pygame.font.SysFont("arial", 36, bold=True)
            text = font.render("GAME OVER - Press R to Restart", True, RED)
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    board = GameBoard()
    board.run()