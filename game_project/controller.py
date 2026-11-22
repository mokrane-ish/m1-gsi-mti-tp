"""
CONTROLLER
----------
Owns the pygame window and the main loop. Reads the keyboard and turns
it into commands on the Model (move_left(), shoot(), ...); it never
draws anything itself and never stores game rules - it only calls the
Model to change state and the View to show it.
"""
import sys
import pygame

from model import GameWorld, SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from view import GameRenderer


class GameController:
    def __init__(self, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT):
        pygame.init()
        pygame.mixer.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("M1 GSI - 2D Game OOP (MVC Refactor)")
        self.clock = pygame.time.Clock()
        self.running = True

        self.world = GameWorld(width, height)
        self.view = GameRenderer(self.screen, width, height)
        self.view.play_music()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.world.status == "game_over":
                    self.world.reset()

        player = self.world.player
        player.tick_cooldown()

        if self.world.status != "playing":
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.move_right()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.move_up()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.move_down()
        player.clamp(self.width, self.height)

        if keys[pygame.K_SPACE] and player.can_shoot():
            self.world.bullets.append(player.shoot())
            self.view.play_shoot_sound()

    def update(self):
        events = self.world.update()
        self.view.play_event_sounds(events)

    def draw(self):
        self.view.draw(self.world)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        self.view.stop_music()
        pygame.quit()
        sys.exit()
