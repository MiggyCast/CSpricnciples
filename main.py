# This file was created by: Miguel Castrillon

"""
New goals: add a powerup that doubles the ship's rate of fire
Another powerup that increases ship movement speed
Goals partly realized
"""

import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRIGHT_GREEN = (0, 255, 0)
NEON_GREEN = (57, 255, 20)

# Player settings
player_size = 50
player_speed = 5
player_fire_rate = 10  # bullets per second
player_fire_delay = 1000 // player_fire_rate

# Enemy settings
enemy_size = 50
enemy_speed = 2
enemy_spawn_delay = 60

# Powerup settings
powerup_size = 30
powerup_speed = 2
powerup_spawn_delay = 5000  # milliseconds
powerup_types = ["fire_rate", "speed"]  # Types of powerups

# Point and lives counters
points = 0
lives = 3
font = pygame.font.Font(None, 36)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Get the current script's directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Full path to the images
player_img_path = os.path.join(script_directory, "rocket.png")
alien_img_path = os.path.join(script_directory, "alien.png")
background_img_path = os.path.join(script_directory, "background.png")
powerup_img_path = os.path.join(script_directory, "powerup.png")

# Load images
player_img = pygame.image.load(player_img_path)
alien_img = pygame.image.load(alien_img_path)
background_img = pygame.image.load(background_img_path)
powerup_img = pygame.image.load(powerup_img_path)

# Scale the images
player_img = pygame.transform.scale(player_img, (player_size, player_size))
alien_img = pygame.transform.scale(alien_img, (enemy_size, enemy_size))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
powerup_img = pygame.transform.scale(powerup_img, (powerup_size, powerup_size))

# Player
player = pygame.Rect(WIDTH // 2 - player_size // 2, HEIGHT - player_size - 10, player_size, player_size)

# Player movement flags
move_left = False
move_right = False
move_up = False
move_down = False

# Enemies
enemies = []

# Bullets
bullets = []

# Powerups
powerups = []

# Functions
def draw_background():
    screen.blit(background_img, (0, 0))

def draw_player():
    screen.blit(player_img, player)

def draw_enemies():
    for enemy in enemies:
        screen.blit(alien_img, enemy)

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, BRIGHT_GREEN, bullet)

def draw_points():
    points_text = font.render(f"Points: {points}", True, WHITE)
    screen.blit(points_text, (10, 10))

def draw_lives():
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (10, 50))

def draw_powerups():
    for powerup in powerups:
        screen.blit(powerup_img, powerup)

def move_player():
    global move_left, move_right, move_up, move_down

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= player_speed
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.y += player_speed

def move_enemies():
    for enemy in enemies:
        enemy.y += enemy_speed

def move_bullets():
    for bullet in bullets:
        bullet.y -= 5

def move_powerups():
    for powerup in powerups:
        powerup.y += powerup_speed

def spawn_enemy():
    enemy = pygame.Rect(random.randint(0, WIDTH - enemy_size), 0, enemy_size, enemy_size)
    enemies.append(enemy)

def spawn_powerup():
    powerup_type = random.choice(powerup_types)
    powerup = pygame.Rect(random.randint(0, WIDTH - powerup_size), 0, powerup_size, powerup_size)
    powerup.type = powerup_type
    powerups.append(powerup)

def check_collision():
    global points, lives

    for bullet in bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                points += 5

    for enemy in enemies:
        if player.colliderect(enemy):
            lives -= 1
            enemies.remove(enemy)

    for powerup in powerups:
        if player.colliderect(powerup):
            apply_powerup_effect(powerup)
            powerups.remove(powerup)

def apply_powerup_effect(powerup):
    global player_fire_delay, player_speed

    if powerup.type == "fire_rate":
        player_fire_delay = max(player_fire_delay // 2, 100)  # Reduce fire delay by half, with a minimum of 100 milliseconds
    elif powerup.type == "speed":
        player_speed = min(player_speed + 2, 10)  # Increase speed by 2, with a maximum of 10

# Main game loop
def main():
    global points, lives
    enemy_spawn_counter = 0
    powerup_spawn_counter = 0

    while lives > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(player.centerx - 2, player.top, 4, 10)
                    bullets.append(bullet)

        move_player()

        screen.fill(BLACK)
        draw_background()
        draw_player()
        draw_enemies()
        draw_bullets()
        draw_points()
        draw_lives()
        draw_powerups()

        move_enemies()
        move_bullets()
        move_powerups()
        check_collision()

        enemy_spawn_counter += 1
        powerup_spawn_counter += 1
        if enemy_spawn_counter == enemy_spawn_delay:
            spawn_enemy()
            enemy_spawn_counter = 0

        if powerup_spawn_counter == powerup_spawn_delay:
            spawn_powerup()
            powerup_spawn_counter = 0

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
