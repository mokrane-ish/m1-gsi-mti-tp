# Game Project Report

## Overview

This project is a 2D Python game built with Pygame and organized using the
Model-View-Controller (MVC) pattern. The player chooses one of three worlds
before gameplay begins. Each world has its own background and monster type.

## Worlds and gameplay

- **Forest:** Chickens move around the level and throw eggs at the player.
- **Graveyard:** Zombies wander randomly and periodically charge directly
  toward the player's current position. The charge starts at a random
  120–300-frame interval and lasts up to 120 frames. Contact deals 20 damage;
  a 45-frame contact cooldown prevents repeated damage every frame while the
  player and zombie overlap. Zombies use this direct charge instead of firing
  the earlier orange projectiles.
- **Classic:** The original background and standard monsters provide a third
  playable world.

Player bullets damage monsters, and defeating monsters increases the score.
Enemy projectiles can damage the player. When player health reaches zero, the
game ends and the current world can be restarted.

## Controls

At the start screen, press:

- **1** to start Forest
- **2** to start Graveyard
- **3** to start Classic

During gameplay, use the **arrow keys** or **WASD** to move and **Space** to
shoot. After game over, press **R** to restart the selected world.

## Architecture and design patterns

- **Model (`model.py`):** Owns game state, monster behavior, damage, scoring,
  movement, collisions, and projectiles. It reports game events without
  playing sounds or drawing.
- **View (`view.py`):** Loads and draws backgrounds and sprites, renders the
  selection screen and game-over display, and plays music and sound effects.
- **Controller (`controller.py`):** Handles input and connects model updates
  to rendering.
- **Factory Method:** `MonsterFactory` creates registered monster types.
- **Abstract Factory:** Each world factory supplies its matching monster type
  and background key.
- **Builder:** `LevelBuilder` and `LevelDirector` assemble the world background
  and starting monster roster.
- **Strategy:** Damage calculators provide different damage rules for monster
  types.

## Audio

- Player shots use `shoot.mp3`.
- Chicken egg throws use `pop.mp3`.
- Chicken hits use `die.mp3`; chicken deaths use `chicken_death.mp3`.
- The zombie sound plays only when a zombie is defeated.
- Background music plays during the game.

## Validation

The Python modules were compiled with `py_compile`. Focused runtime checks
using Pygame's dummy SDL drivers covered world selection, world-specific
monster creation, zombie movement and charging, contact damage, and the zombie
death sound event. These checks do not replace testing the game interactively
with a display.
