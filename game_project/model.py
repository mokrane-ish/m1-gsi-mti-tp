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
import random
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
    """A projectile fired downward by a Shootable monster. Pure state.

    `kind` lets the View pick the right sprite ("egg" for the Chicken's
    thrown egg, or a plain shape for anything else) without this class
    needing to know what an image is.
    """

    WIDTH = 10
    HEIGHT = 20
    EGG_WIDTH = 22
    EGG_HEIGHT = 28

    def __init__(self, x: int, y: int, kind: str = "generic"):
        self.kind = kind
        if kind == "egg":
            w, h = self.EGG_WIDTH, self.EGG_HEIGHT
        else:
            w, h = self.WIDTH, self.HEIGHT
        self.rect = pygame.Rect(x - w // 2, y, w, h)
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
    # How many frames a dead monster stays in world.monsters (and thus
    # visible) after dying. 0 = vanish immediately (old TP3 behaviour).
    # ChickenMonster raises this so the View has time to show chicken-die.png.
    DEATH_LINGER_FRAMES = 0

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
        self.death_timer = 0
        self.damage_calculator = damage_calculator or StandardDamageCalculator()

    def take_damage(self, weapon_type: str, base_damage: float):
        """Apply damage calculated via the injected DamageCalculator (DIP)."""
        if not self.is_alive:
            return
        final_damage = self.damage_calculator.calculate_damage(weapon_type, base_damage)
        self.health = max(0.0, self.health - final_damage)
        if self.health == 0:
            self.is_alive = False
            self.death_timer = self.DEATH_LINGER_FRAMES

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


# ----------------------------------------------------------
# 5bis. New for this workshop: Zombie (Graveyard) & Chicken (Forest)
# ----------------------------------------------------------
class ZombieMonster(Monster, Movable):
    """Graveyard monster that wanders, charges the player, and damages on contact."""

    def __init__(self, x: int, y: int, speed_x: int = 2):
        super().__init__(x=x, y=y, label="Zombie", max_health=120.0,
                          damage_calculator=WeaponResistantCalculator(resistant_to="bullet", multiplier=0.7))
        self.speed = speed_x
        self.direction_x = 0
        self.direction_y = 0
        self.direction_timer = 0
        self.attack_timer = random.randint(120, 300)
        self.is_charging = False
        self.charge_timer = 0
        self.contact_cooldown = 0

    def move(
        self,
        screen_width: int,
        screen_height: int = SCREEN_HEIGHT,
        player: Player = None,
    ):
        if self.is_charging and player is not None:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            distance = math.hypot(dx, dy)
            if distance:
                charge_speed = self.speed * 2
                self.rect.x += round(dx / distance * charge_speed)
                self.rect.y += round(dy / distance * charge_speed)
                self.rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_height))
            return

        if self.direction_timer <= 0:
            self.direction_x, self.direction_y = random.choice(
                [
                    (-1, -1), (0, -1), (1, -1),
                    (-1, 0),             (1, 0),
                    (-1, 1),  (0, 1),  (1, 1),
                ]
            )
            self.direction_timer = random.randint(30, 90)

        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed
        self.rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_height))
        if self.rect.left == 0 and self.direction_x < 0:
            self.direction_x *= -1
        elif self.rect.right == screen_width and self.direction_x > 0:
            self.direction_x *= -1
        if self.rect.top == 0 and self.direction_y < 0:
            self.direction_y *= -1
        elif self.rect.bottom == screen_height and self.direction_y > 0:
            self.direction_y *= -1
        self.direction_timer -= 1

    def finish_attack(self):
        self.is_charging = False
        self.charge_timer = 0
        self.attack_timer = random.randint(120, 300)
        self.direction_timer = 0

    def update(self, screen_width: int, screen_height: int, enemy_bullets: list, player: Player = None):
        if not self.is_alive:
            return

        if self.contact_cooldown > 0:
            self.contact_cooldown -= 1

        if not self.is_charging:
            self.attack_timer -= 1
            if self.attack_timer <= 0 and player is not None:
                self.is_charging = True
                self.charge_timer = 120

        self.move(screen_width, screen_height, player)
        if self.is_charging:
            self.charge_timer -= 1
            if self.charge_timer <= 0:
                self.finish_attack()


class ChickenMonster(Monster, Movable, Shootable):
    """Forest-world monster: fast and fragile, throws eggs at the player."""

    # Stay on screen a little after dying so the View can show chicken-die.png.
    DEATH_LINGER_FRAMES = 40

    def __init__(self, x: int, y: int, speed_x: int = 5):
        super().__init__(x=x, y=y, label="Chicken", max_health=60.0,
                          damage_calculator=StandardDamageCalculator())
        self.speed_x = speed_x
        self.throw_cooldown = 100

    def move(self, screen_width: int):
        self.rect.x += self.speed_x
        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.speed_x *= -1

    def shoot(self, enemy_bullets: list):
        """'Shoot' here means throw an egg - same Shootable contract as
        ShooterMonster, just a different projectile kind."""
        self.throw_cooldown -= 1
        if self.throw_cooldown <= 0:
            enemy_bullets.append(EnemyBullet(self.rect.centerx, self.rect.bottom, kind="egg"))
            self.throw_cooldown = 100

    def update(self, screen_width: int, screen_height: int, enemy_bullets: list):
        if self.is_alive:
            self.move(screen_width)
            self.shoot(enemy_bullets)


# ==========================================================
# 6. Factory Method: create a monster by name, on demand
# ==========================================================
class MonsterFactory:
    """Centralizes monster creation. Both the starting roster and any
    monster spawned later in the level go through create_monster(), so
    adding a new kind never means touching GameWorld's logic."""

    _REGISTRY = {
        "normal": NormalMonster,
        "fast": FastMonster,
        "flying": FlyingMonster,
        "strong": StrongMonster,
        "immobile": ImmobileMonster,
        "shooter": ShooterMonster,
        "zombie": ZombieMonster,
        "chicken": ChickenMonster,
    }

    @staticmethod
    def create_monster(kind: str, x: int, y: int) -> Monster:
        monster_cls = MonsterFactory._REGISTRY.get(kind.lower())
        if monster_cls is None:
            raise ValueError(f"MonsterFactory cannot create unknown kind: {kind}")
        return monster_cls(x, y)


# ==========================================================
# 7. Abstract Factory: a "world" is a family of compatible pieces
# ==========================================================
class WorldFactory(ABC):
    """A world bundles the one monster kind that belongs in it and the
    background that goes with it. Two worlds never mix their monsters."""

    name: str = "world"
    monster_kind: str = "normal"
    background_key: str = "forest"

    def create_monster(self, x: int, y: int) -> Monster:
        """Delegates to the Factory Method above - an Abstract Factory
        is free to build on top of another creational pattern."""
        return MonsterFactory.create_monster(self.monster_kind, x, y)


class GraveyardWorldFactory(WorldFactory):
    name = "graveyard"
    monster_kind = "zombie"
    background_key = "graveyard"


class ForestWorldFactory(WorldFactory):
    name = "forest"
    monster_kind = "chicken"
    background_key = "forest"


class ClassicWorldFactory(WorldFactory):
    name = "classic"
    monster_kind = "normal"
    background_key = "classic"


WORLD_FACTORIES = {
    "classic": ClassicWorldFactory(),
    "graveyard": GraveyardWorldFactory(),
    "forest": ForestWorldFactory(),
}


# ==========================================================
# 8. Builder: assemble a level step by step from a WorldFactory
# ==========================================================
class Level:
    """The finished product of a LevelBuilder: a background key and a
    ready-to-use list of monsters."""

    def __init__(self):
        self.background_key: str = "forest"
        self.monsters: list = []


class LevelBuilder:
    """Builds a Level one step at a time (background, then monsters),
    exactly like Part 4's Story/Builder exercise."""

    # Fixed spawn points shared by every world, so levels stay comparable.
    SPAWN_POINTS = [(460, 35), (120, 95), (680, 155), (320, 120), (760, 60), (200, 200)]

    def __init__(self):
        self._level = Level()

    def reset(self):
        self._level = Level()
        return self

    def set_background(self, factory: WorldFactory):
        self._level.background_key = factory.background_key
        return self

    def add_monsters(self, factory: WorldFactory, positions=None):
        for (x, y) in (positions or self.SPAWN_POINTS):
            self._level.monsters.append(factory.create_monster(x, y))
        return self

    def get_level(self) -> Level:
        return self._level


class LevelDirector:
    """Knows the recipe: background first, then the monster roster."""

    def __init__(self, builder: LevelBuilder):
        self.builder = builder

    def construct(self, factory: WorldFactory) -> Level:
        self.builder.reset().set_background(factory).add_monsters(factory)
        return self.builder.get_level()


# ==========================================================
# 9. GameWorld: all game logic for one frame (the "M" of MVC)
# ==========================================================
class GameWorld:
    """Holds every game object and the rules that update them each frame.
    Knows nothing about pygame windows, images, sounds or the keyboard.
    Produces a list of event names (strings) so the View/Controller can
    react (e.g. play a sound) without the Model depending on audio."""

    # A new monster of the current world is spawned this often (Factory
    # Method in action during play, not just at level start).
    SPAWN_INTERVAL_FRAMES = 240

    def __init__(self, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT):
        self.width = width
        self.height = height
        self.player: Player = None
        self.monsters: list = []
        self.bullets: list = []
        self.enemy_bullets: list = []
        self.score = 0
        self.status = "menu"  # "menu", "playing", or "game_over"
        self.current_world = None
        self.spawn_timer = self.SPAWN_INTERVAL_FRAMES

    def set_world(self, world_name: str):
        """Rebuild the whole level for the given world, using the
        Builder (LevelDirector + LevelBuilder) on top of that world's
        Abstract Factory."""
        factory = WORLD_FACTORIES[world_name]
        level = LevelDirector(LevelBuilder()).construct(factory)

        self.current_world = world_name
        self.player = Player(x=460, y=490)
        self.monsters = level.monsters
        self.bullets.clear()
        self.enemy_bullets.clear()
        self.score = 0
        self.status = "playing"
        self.spawn_timer = self.SPAWN_INTERVAL_FRAMES

    def reset(self):
        """Restart the current world (used by the Controller's 'R' key)."""
        self.set_world(self.current_world)

    def _spawn_extra_monster(self):
        """Factory Method used again mid-game: a fresh monster of the
        active world's kind appears at a random edge position."""
        factory = WORLD_FACTORIES[self.current_world]
        x = random.choice([40, self.width - 40 - Monster.WIDTH])
        y = random.randint(40, self.height // 2)
        self.monsters.append(factory.create_monster(x, y))

    def update(self) -> list:
        """Advance the world by one frame. Returns a list of event names
        such as 'chicken_hit', 'chicken_killed', 'chicken_throw',
        'zombie_hit', 'zombie_killed', 'player_hit', 'player_died'."""
        events = []

        if self.status != "playing":
            return events

        # Occasionally spawn a new monster of the current world's kind.
        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self._spawn_extra_monster()
            self.spawn_timer = self.SPAWN_INTERVAL_FRAMES

        # Update all monsters polymorphically (LSP); dead ones just tick
        # down their death_timer (if any) instead of acting.
        enemy_bullets_before = len(self.enemy_bullets)
        for monster in self.monsters:
            if monster.is_alive:
                if isinstance(monster, ZombieMonster):
                    monster.update(self.width, self.height, self.enemy_bullets, self.player)
                else:
                    monster.update(self.width, self.height, self.enemy_bullets)
            elif monster.death_timer > 0:
                monster.death_timer -= 1

        # Any enemy bullet that appeared this frame was just thrown/fired.
        for new_bullet in self.enemy_bullets[enemy_bullets_before:]:
            if new_bullet.kind == "egg":
                events.append("chicken_throw")

        # Drop fully-expired dead monsters from the world.
        self.monsters = [m for m in self.monsters if m.is_alive or m.death_timer > 0]

        # A zombie touching the player deals the same damage as a projectile hit.
        for monster in self.monsters:
            if (
                isinstance(monster, ZombieMonster)
                and monster.is_alive
                and self.player.is_alive
                and monster.rect.colliderect(self.player.rect)
            ):
                if monster.is_charging:
                    monster.finish_attack()
                if monster.contact_cooldown == 0:
                    self.player.take_damage(20)
                    monster.contact_cooldown = 45
                    events.append("player_hit")
                    if not self.player.is_alive:
                        self.status = "game_over"
                        events.append("player_died")
                    break

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
                    tag = monster.label.lower()
                    if not monster.is_alive:
                        self.score += int(monster.max_health)
                        events.append(f"{tag}_killed")
                    else:
                        events.append(f"{tag}_hit")
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
