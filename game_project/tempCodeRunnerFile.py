 def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.world.status == "game_over":
                    self.world.reset()
                # Switch world at any time: rebuilds the level via the
                # Builder on top of that world's Abstract Factory.
                elif event.key == pygame.K_1:
                    self.world.set_world("forest")
                elif event.key == pygame.K_2:
                    self.world.set_world("graveyard")