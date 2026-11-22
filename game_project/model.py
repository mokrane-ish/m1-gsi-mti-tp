"""
MODEL
-----
Game state and game logic only: positions, health, damage, scoring,
collisions. Nothing here loads an image, plays a sound, or reads the
keyboard - that is the job of the View and the Controller. The only
thing borrowed from pygame is pygame.Rect, used purely as a small
x/y/width/height box for collision math (colliderect), not for drawing.
"""
import math
from abc import ABC, abstractmethod
import pygame

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60


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
# 3. Projectiles & Player (state only - no image, no sound)
# ==========================================================
class Bullet:
    """A projectile shot by the Player. Pure state, no rendering."""

    WIDTH = 20
    HEIGHT = 32

    def __init__(self, x: int, y: int, weapon_type: str = "bullet", damage: float = 25.0):
        self.rect = pygame.Rect(x - self.WIDTH // 2, y, self.WIDTH, self.HEIGHT)
        self.speed = 8
        self.weapon_type = weapon_type
        self.damage = damage
        self.is_active = True

    def update(self):
        """Move projectile upward and deactivate when off-screen."""
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.is_active = False


class EnemyBullet:
    """A projectile fired downward by a Shootable monster. Pure state."""

    WIDTH = 10
    HEIGHT = 20

    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x - self.WIDTH // 2, y, self.WIDTH, self.HEIGHT)
        self.speed = 5
        self.is_active = True

    def update(self, screen_height: int):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.is_active = False


class Player:
    """The player. Holds state and reacts to commands; never reads the
    keyboard itself (the Controller does that and calls these methods)."""

    WIDTH = 80
    HEIGHT = 80

    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)
        self.speed = 5
        self.cooldown = 0

        self.label = "Player"
        self.max_health = 100
        self.health = 100
        self.is_alive = True

    def take_damage(self, amount: int):
        if not self.is_alive:
            return
        self.health = max(0, self.health - amount)
        if self.health == 0:
            self.is_alive = False

    # --- Movement commands (called by the Controller) ---
    def move_left(self):
        self.rect.x -= self.speed

    def move_right(self):
        self.rect.x += self.speed

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def clamp(self, screen_width: int, screen_height: int):
        self.rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_height))

    # --- Shooting ---
    def tick_cooldown(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def can_shoot(self) -> bool:
        return self.is_alive and self.cooldown == 0

    def shoot(self) -> "Bullet":
        """Create and return a new Bullet, and reset the cooldown."""
        self.cooldown = 15
        return Bullet(self.rect.centerx, self.rect.top)


# ==========================================================
# 4. SRP & LSP: Core Monster Base Class (No Rendering Logic)
# ==========================================================
class Monster:
    """Base enemy class responsible only for state, health, and damage handling."""

    WIDTH = 75
    HEIGHT = 75

    def __init__(
        self,
        x: int,
        y: int,
        label: str = "Monster",
        max_health: float = 100.0,
        damage_calculator: DamageCalculator = None,
    ):
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)
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
        super().__init__(x=x, y=y, label="Normal", max_health=100.0,
                          damage_calculator=StandardDamageCalculator())
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
        super().__init__(x=x, y=y, label="Fast", max_health=75.0,
                          damage_calculator=WeaponWeaknessCalculator(weak_to="bullet", multiplier=1.5))
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
        super().__init__(x=x, y=y, label="Flying", max_health=100.0,
                          damage_calculator=StandardDamageCalculator())
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
        super().__init__(x=x, y=y, label="Strong", max_health=150.0,
                          damage_calculator=WeaponResistantCalculator(resistant_to="bullet", multiplier=0.5))
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
        super().__init__(x=x, y=y, label="Immobile", max_health=100.0,
                          damage_calculator=StandardDamageCalculator())


class ShooterMonster(Monster, Movable, Shootable):
    """Monster that patrols and periodically fires projectiles downward."""

    def __init__(self, x: int, y: int, speed_x: int = 3):
        super().__init__(x=x, y=y, label="Shooter", max_health=100.0,
                          damage_calculator=StandardDamageCalculator())
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
# 6. GameWorld: all game logic for one frame (the "M" of MVC)
# ==========================================================
class GameWorld:
    """Holds every game object and the rules that update them each frame.
    Knows nothing about pygame windows, images, sounds or the keyboard.
    Produces a list of event names (strings) so the View/Controller can
    react (e.g. play a sound) without the Model depending on audio."""

    def __init__(self, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT):
        self.width = width
        self.height = height
        self.player: Player = None
        self.monsters: list[Monster] = []
        self.bullets: list[Bullet] = []
        self.enemy_bullets: list[EnemyBullet] = []
        self.score = 0
        self.status = "playing"  # or "game_over"
        self.reset()

    def reset(self):
        """(Re)initialize player, monsters, projectiles and score."""
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
        self.score = 0
        self.status = "playing"

    def update(self) -> list:
        """Advance the world by one frame. Returns a list of event names
        such as 'monster_killed', 'player_hit', 'player_died'."""
        events = []

        if self.status != "playing":
            return events

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
                        self.score += int(monster.max_health)
                        events.append("monster_killed")
                    break

        # Update enemy bullets and check collisions with the player
        for e_bullet in self.enemy_bullets[:]:
            e_bullet.update(self.height)
            if not e_bullet.is_active:
                self.enemy_bullets.remove(e_bullet)
            elif self.player.is_alive and e_bullet.rect.colliderect(self.player.rect):
                self.player.take_damage(20)
                self.enemy_bullets.remove(e_bullet)
                events.append("player_hit")
                if not self.player.is_alive:
                    self.status = "game_over"
                    events.append("player_died")

        return events
