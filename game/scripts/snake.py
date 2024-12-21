################################################################################
#region Imports


# Third Party
import pygame


# Local
from scripts.constants import RIGHT, CELL_SIZE, BORDER_THICKNESS, GRID_WIDTH, GRID_HEIGHT


#endregion
################################################################################
#region Snake (Player)


class Snake:
    """
    Handles the snake object for the game.

    Attributes:
        body (list): The list of body segments.
        direction (tuple): The current direction the snake is moving.
        growing (bool): Whether the snake is growing.
        theme (Theme): The current theme.

    Methods:
        move: Move the snake in the current direction.
        grow: Grow the snake by one segment.
        draw: Draw the snake on the screen.
        draw_snake_body: Draw the snake body on the screen.
        draw_snake_head: Draw the snake head on the screen.
        _blend_colors: Blend two colors together by a factor.

    """

    def __init__(self, theme):
        self.body = [(10, 10)]
        self.direction = RIGHT
        self.growing = False
        self.theme = theme


    def move(self, peaceful_mode=False):
        """Move snake by one step."""
        new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
        if peaceful_mode:
            new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)
        self.body.insert(0, new_head)
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False


    def grow(self):
        """Grow the snake by one segment."""
        self.growing = True


    def draw(self, surface):
        """Draw the snake on the screen."""
        self.draw_snake_body(surface)
        self.draw_snake_head(surface)  # Draw head last so it's always on top


    def draw_snake_body(self, surface):
        """Draw the snake body."""
        if len(self.body) > 1:
            # Draw segments in reverse order so later segments appear on top
            for i, segment in enumerate(reversed(self.body[1:])):
                x, y = segment
                # Calculate gradient from tail to neck
                gradient_factor = (len(self.body) - 2 - i) / (len(self.body) - 1)
                body_color = self._blend_colors(self.theme.body_color, self.theme.tail_color, gradient_factor)
                pygame.draw.rect(surface, body_color, pygame.Rect(x * CELL_SIZE + BORDER_THICKNESS, y * CELL_SIZE + BORDER_THICKNESS, CELL_SIZE, CELL_SIZE))


    def draw_snake_head(self, surface):
        """Draw the snake head."""
        head = self.body[0]
        x, y = head
        pygame.draw.rect(surface, self.theme.head_color, pygame.Rect(x * CELL_SIZE + BORDER_THICKNESS, y * CELL_SIZE + BORDER_THICKNESS, CELL_SIZE, CELL_SIZE))


    def _blend_colors(self, color1, color2, factor):
        """Blend two colors together by a factor (0 to 1)."""
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        return r, g, b
