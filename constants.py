import pygame

pygame.init()

# Game sizes
GAME_WIDTH = 800
GAME_HEIGHT = 600
CELL_WIDTH = 32
CELL_HEIGHT = 32

# Map Variables
MAP_WIDTH = 30
MAP_HEIGHT = 30

# Color definitions
COLOR_BLACK = (0,   0,   0)
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY  = (100, 100, 100)

# Game colors
COLOR_DEFAULT_BG = COLOR_GRAY

# Sprites
S_PLAYER = pygame.image.load("Assets/Main_Player.png")
S_ENEMY = pygame.image.load("Assets/Enemy_1.png")
S_WALL = pygame.image.load("Assets/Wall_1.png")
S_FLOOR = pygame.image.load("Assets/Floor.png")

# Sprites: https://imgur.com/a/TECi6
