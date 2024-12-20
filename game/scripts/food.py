
################################################################################
#region Imports


# Standard Library
import random


# Third Party
import pygame


# Local
from scripts.constants import GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, BORDER_THICKNESS


#endregion
################################################################################
#region Food


class Food:
    """
    Class for the food object.

    Attributes:
        theme (Theme): The theme for the game.
        position (tuple): The position of the food.

    Methods:
        random_position: Generate a random position for the food.
        draw: Draw the food on the screen.

    """

    def __init__(self, theme, snake):
        self.theme = theme
        self.position = self.random_position(snake)


    def random_position(self, snake):
        """Generate a random position for the food, not on the snake."""
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake.body:
                return pos


    def draw(self, surface):
        """Draw the food on the screen."""
        x, y = self.position
        pygame.draw.rect(surface, self.theme.food_color,
            pygame.Rect(x * CELL_SIZE + BORDER_THICKNESS,
                y * CELL_SIZE + BORDER_THICKNESS,
                CELL_SIZE, CELL_SIZE))
