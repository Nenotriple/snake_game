################################################################################
#region Imports


# Third Party
import pygame


# Local
from scripts.constants import WHITE, BLACK


#endregion
################################################################################
#region draw_text


# Offsets for the text outline
OFFSETS = [(1, 1), (-1, -1), (-1, 1), (1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]


def draw_text(surface, text, size, x, y, color=WHITE):
    """Draw text with an outline on a surface."""
    font = _create_font(size)
    _draw_text_outline(surface, text, x, y, font)
    _draw_main_text(surface, text, x, y, color, font)


def _create_font(size):
    """Create a font object."""
    font = pygame.font.Font(None, size)
    return font


def _draw_text_outline(surface, text, x, y, font):
    """Draw the outline text on the surface."""
    for offset_x, offset_y in OFFSETS:
        outline_surface = font.render(text, True, BLACK)
        outline_rect = outline_surface.get_rect(center=(x + offset_x, y + offset_y))
        surface.blit(outline_surface, outline_rect)


def _draw_main_text(surface, text, x, y, color, font):
    """Draw the main text on the surface."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)
