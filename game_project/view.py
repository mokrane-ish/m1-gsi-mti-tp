"""
VIEW
----
Everything about *how the game looks and sounds*: loading images and
sounds, and drawing the current state of the Model to the screen. This
module never changes game state and never reads the keyboard - it only
reads the Model's public attributes (rect, health, label, score, ...).

Changing the look of the game (a new player.png, a new background.jpg,
...) only means replacing a file under assets/ - nothing in this file
or in model.py needs to change.
"""
import os
import pygame
from model import Shieldable, ZombieMonster, ChickenMonster

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

PLAYER_IMAGE_PATH = os.path.join(ASSETS_DIR, "player", "player.png")
MONSTER_IMAGE_PATH = os.path.join(ASSETS_DIR, "monsters", "monster.png")
ZOMBIE_IMAGE_PATH = os.path.join(ASSETS_DIR, "monsters", "zombie.png")
CHICKEN_IMAGE_PATH = os.path.join(ASSETS_DIR, "monsters", "chicken.png")
CHICKEN_DIE_IMAGE_PATH = os.path.join(ASSETS_DIR, "monsters", "chicken-die.png")

BULLET_IMAGE_PATH = os.path.join(ASSETS_DIR, "bullets", "bulet.png")
EGG_IMAGE_PATH = os.path.join(ASSETS_DIR, "bullets", "egg.png")

FOREST_BACKGROUND_PATH = os.path.join(ASSETS_DIR, "backgrounds", "background_forest.jpg")
GRAVEYARD_BACKGROUND_PATH = os.path.join(ASSETS_DIR, "backgrounds", "background_graveyard.jpg")
CLASSIC_BACKGROUND_PATH = os.path.join(ASSETS_DIR, "backgrounds", "background.jpg")

SHOOT_SOUND_PATH = os.path.join(ASSETS_DIR, "sounds", "shoot.mp3")
CHICKEN_HIT_SOUND_PATH = os.path.join(ASSETS_DIR, "sounds", "chicken_death.mp3")
CHICKEN_DEATH_SOUND_PATH = os.path.join(ASSETS_DIR, "sounds", "chicken_death.mp3")
EGG_THROW_SOUND_PATH = os.path.join(ASSETS_DIR, "sounds", "pop.mp3")
ZOMBIE_SOUND_PATH = os.path.join(ASSETS_DIR, "sounds", "zombie_sound.mp3")
MUSIC_PATH = os.path.join(ASSETS_DIR, "sounds", "music.mp3")

# Colors (RGB)
RED = (220, 50, 50)
GREEN = (50, 220, 80)
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40)
CYAN = (80, 220, 255)
ORANGE = (255, 140, 0)


class GameRenderer:
    """Loads every asset once, then draws the GameWorld each frame."""

    def __init__(self, screen: pygame.Surface, width: int, height: int):
        self.screen = screen
        self.width = width
        self.height = height

        # --- Backgrounds, one per world (chosen in draw_background) ---
        self.backgrounds = {
            "classic": self._load_background(CLASSIC_BACKGROUND_PATH),
            "forest": self._load_background(FOREST_BACKGROUND_PATH),
            "graveyard": self._load_background(GRAVEYARD_BACKGROUND_PATH),
        }

        # --- Sprites (raw, unscaled - scaled per entity at draw time) ---
        self.player_image = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
        self.monster_image = pygame.image.load(MONSTER_IMAGE_PATH).convert_alpha()
        self.zombie_image = pygame.image.load(ZOMBIE_IMAGE_PATH).convert_alpha()
        self.chicken_image = pygame.image.load(CHICKEN_IMAGE_PATH).convert_alpha()
        self.chicken_die_image = pygame.image.load(CHICKEN_DIE_IMAGE_PATH).convert_alpha()

        self.bullet_image = pygame.image.load(BULLET_IMAGE_PATH).convert_alpha()
        self.egg_image = pygame.image.load(EGG_IMAGE_PATH).convert_alpha()

        # --- Sounds ---
        self.shoot_sound = self._load_sound(SHOOT_SOUND_PATH, 0.5)
        self.chicken_hit_sound = self._load_sound(CHICKEN_HIT_SOUND_PATH, 0.6)
        self.chicken_death_sound = self._load_sound(CHICKEN_DEATH_SOUND_PATH, 0.7)
        self.egg_throw_sound = self._load_sound(EGG_THROW_SOUND_PATH, 0.6)
        self.zombie_sound = self._load_sound(ZOMBIE_SOUND_PATH, 0.6)

        # --- Fonts ---
        self.label_font = pygame.font.SysFont("arial", 13, bold=True)
        self.panel_font = pygame.font.SysFont("arial", 18, bold=True)
        self.overlay_font = pygame.font.SysFont("arial", 36, bold=True)
        self.menu_option_font = pygame.font.SysFont("arial", 24, bold=True)

    def _load_background(self, path):
        image = pygame.image.load(path).convert()
        return pygame.transform.scale(image, (self.width, self.height))

    @staticmethod
    def _load_sound(path, volume):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        return sound

    # --- Music ---
    def play_music(self):
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    # --- Sound effects, triggered from Model events or input ---
    def play_shoot_sound(self):
        self.shoot_sound.play()

    def play_event_sounds(self, events: list):
        """Each event name coming out of GameWorld.update() maps to at
        most one sound here - the Model never touches pygame.mixer."""
        if "chicken_throw" in events:
            self.egg_throw_sound.play()
        if "chicken_hit" in events:
            self.chicken_hit_sound.play()
        if "chicken_killed" in events:
            self.chicken_death_sound.play()
        if "zombie_killed" in events:
            self.zombie_sound.play()

    # --- Drawing ---
    def draw_background(self, world):
        self.screen.blit(self.backgrounds[world.current_world], (0, 0))

    def draw_player(self, player):
        if player.is_alive:
            sprite = pygame.transform.scale(self.player_image, player.rect.size)
            self.screen.blit(sprite, player.rect)

    def _sprite_for(self, monster):
        if isinstance(monster, ZombieMonster):
            return self.zombie_image
        if isinstance(monster, ChickenMonster):
            return self.chicken_image
        return self.monster_image

    def draw_monster(self, monster):
        if monster.is_alive:
            sprite = pygame.transform.scale(self._sprite_for(monster), monster.rect.size)
            self.screen.blit(sprite, monster.rect)
            if isinstance(monster, Shieldable) and monster.has_active_shield():
                pygame.draw.ellipse(self.screen, CYAN, monster.rect.inflate(10, 10), width=2)
        elif isinstance(monster, ChickenMonster) and monster.death_timer > 0:
            # Lingers for a moment showing the "plucked" sprite, then vanishes.
            sprite = pygame.transform.scale(self.chicken_die_image, monster.rect.size)
            self.screen.blit(sprite, monster.rect)

    def draw_bullet(self, bullet):
        sprite = pygame.transform.scale(self.bullet_image, bullet.rect.size)
        self.screen.blit(sprite, bullet.rect)

    def draw_enemy_bullet(self, enemy_bullet):
        if enemy_bullet.kind == "egg":
            sprite = pygame.transform.scale(self.egg_image, enemy_bullet.rect.size)
            self.screen.blit(sprite, enemy_bullet.rect)
        else:
            # No dedicated sprite for this projectile kind: a plain shape is enough.
            pygame.draw.rect(self.screen, ORANGE, enemy_bullet.rect, border_radius=4)

    def draw_health_bar(self, entity):
        if not entity.is_alive:
            return

        bar_width = entity.rect.width
        bar_height = 7
        bar_x = entity.rect.x
        bar_y = max(18, entity.rect.y - 12)

        label_surface = self.label_font.render(entity.label, True, WHITE)
        label_rect = label_surface.get_rect(centerx=entity.rect.centerx, bottom=bar_y - 2)
        self.screen.blit(label_surface, label_rect)

        pygame.draw.rect(self.screen, RED, (bar_x, bar_y, bar_width, bar_height))
        health_ratio = entity.health / entity.max_health if entity.max_health > 0 else 0
        current_width = int(bar_width * health_ratio)
        pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, current_width, bar_height))
        pygame.draw.rect(self.screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height), width=1)

    def draw_info_panel(self, world):
        """Top-left panel: score, player health, world and game status."""
        status_text = "Playing" if world.status == "playing" else "Game Over"
        lines = [
            f"World: {world.current_world.capitalize()}",
            f"Score: {world.score}",
            f"Health: {int(world.player.health)}/{int(world.player.max_health)}",
            f"Status: {status_text}",
        ]
        panel_width, line_height, padding = 200, 22, 8
        panel_height = len(lines) * line_height + padding
        panel = pygame.Surface((panel_width, panel_height))
        panel.set_alpha(160)
        panel.fill(DARK_GRAY)
        self.screen.blit(panel, (10, 10))

        for i, line in enumerate(lines):
            text_surface = self.panel_font.render(line, True, WHITE)
            self.screen.blit(text_surface, (10 + padding // 2, 10 + padding // 2 + i * line_height))

    def draw_game_over_overlay(self):
        text = self.overlay_font.render("GAME OVER - Press R to Restart", True, RED)
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, text_rect)

    def draw_world_selection(self):
        self.screen.blit(self.backgrounds["classic"], (0, 0))

        panel = pygame.Surface((540, 330))
        panel.set_alpha(205)
        panel.fill(DARK_GRAY)
        panel_rect = panel.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(panel, panel_rect)

        title = self.overlay_font.render("Choose Your World", True, WHITE)
        self.screen.blit(title, title.get_rect(center=(self.width // 2, panel_rect.y + 55)))

        subtitle = self.panel_font.render("Press a number to start playing", True, WHITE)
        self.screen.blit(subtitle, subtitle.get_rect(center=(self.width // 2, panel_rect.y + 112)))

        options = (
            "1 - Forest (Chickens)",
            "2 - Graveyard (Zombies)",
            "3 - Classic (Monsters)",
        )
        for index, option in enumerate(options):
            text = self.menu_option_font.render(option, True, WHITE)
            self.screen.blit(text, text.get_rect(center=(self.width // 2, panel_rect.y + 170 + index * 45)))

        pygame.display.flip()

    def draw(self, world):
        """Draw one full frame from the current state of the GameWorld."""
        self.draw_background(world)

        self.draw_player(world.player)
        self.draw_health_bar(world.player)

        for monster in world.monsters:
            self.draw_monster(monster)
            self.draw_health_bar(monster)

        for bullet in world.bullets:
            self.draw_bullet(bullet)

        for e_bullet in world.enemy_bullets:
            self.draw_enemy_bullet(e_bullet)

        self.draw_info_panel(world)

        if world.status == "game_over":
            self.draw_game_over_overlay()

        pygame.display.flip()
