"""This module contains the constants used in the game."""


# Constants
GRID_WIDTH = 36
GRID_HEIGHT = 24
CELL_SIZE = 20
BORDER_THICKNESS = 20
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE + (2 * BORDER_THICKNESS)
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE + (2 * BORDER_THICKNESS)
BASE_FPS = 10


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)


# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
