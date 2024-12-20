"""

This module contains the classes for the different game states.


Classes:
    GameState: Enum class for the different game states.
    Difficulty: Enum class for the different game difficulties.
    MainMenu: Class for the main menu.
    PauseMenu: Class for the pause menu.
    GameOver: Class for the game over screen.

"""

################################################################################
#region Imports


# Standard Library
from enum import Enum


# Third Party
import pygame


# Local
from scripts.constants import WHITE, YELLOW
from scripts.theme import Theme
from scripts.draw_text import draw_text


#endregion
################################################################################
#region GameState


class GameState(Enum):
    """For tracking the current state of the game."""
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4


class Difficulty(Enum):
    """For tracking the difficulty of the game."""
    EASY = 0.0
    MEDIUM = 0.00375
    HARD = 0.0175


#endregion
################################################################################
#region MainMenu


class MainMenu:
    """
    Handle the main menu of the game.

    Attributes:
        screen_width (int): The width of the screen.
        screen_height (int): The height of the screen.
        themes (list): List of available themes.
        selected_theme_index (int): Index of the selected theme.
        difficulties (list): List of available difficulties.
        selected_difficulty (Difficulty): The selected difficulty.
        menu_options (list): List of menu options.
        selected_option (int): Index of the selected option.

    Methods:
        handle_input: Handle input events for the main menu.
        draw: Draw the main menu on the screen.
    """

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.themes = Theme.get_themes()
        self.selected_theme_index = 0
        self.difficulties = list(Difficulty)
        self.selected_difficulty = Difficulty.MEDIUM
        self.menu_options = ["Play", "Difficulty", "Theme", "Exit"]
        self.selected_option = 0


# --------------------------------------
# Input
# --------------------------------------
    def handle_input(self, event):
        """Handle input events for the main menu."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.menu_options[self.selected_option] == "Play":
                    return GameState.PLAYING, self.selected_theme_index, self.selected_difficulty
                elif self.menu_options[self.selected_option] == "Exit":
                    pygame.quit()
                    exit()
            elif event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                if self.menu_options[self.selected_option] == "Theme":
                    self._change_theme(event)
                elif self.menu_options[self.selected_option] == "Difficulty":
                    self._change_difficulty(event)
        return GameState.MENU, self.selected_theme_index, self.selected_difficulty


    def _change_theme(self, event):
        """Change the selected theme based on the input event."""
        if event.key == pygame.K_LEFT:
            self.selected_theme_index = (self.selected_theme_index - 1) % len(self.themes)
        else:
            self.selected_theme_index = (self.selected_theme_index + 1) % len(self.themes)


    def _change_difficulty(self, event):
        """Change the selected difficulty based on the input event."""
        current_idx = self.difficulties.index(self.selected_difficulty)
        if event.key == pygame.K_LEFT:
            self.selected_difficulty = self.difficulties[(current_idx - 1) % len(self.difficulties)]
        else:
            self.selected_difficulty = self.difficulties[(current_idx + 1) % len(self.difficulties)]


# --------------------------------------
# Draw
# --------------------------------------
    def draw(self, surface):
        """Draw the main menu on the screen."""
        self._draw_title(surface)
        self._draw_menu_options(surface)
        self._draw_instructions(surface)


    def _draw_title(self, surface):
        """Draw the title on the screen."""
        draw_text(surface, "SNAKE", 64, self.screen_width // 2, 60)


    def _draw_menu_options(self, surface):
        """Draw the menu options on the screen."""
        start_y = self.screen_height // 2 + 80
        for i, option in enumerate(self.menu_options):
            color = YELLOW if i == self.selected_option else WHITE
            if option == "Theme":
                text = f"Theme: {self.themes[self.selected_theme_index].name}"
            elif option == "Difficulty":
                text = f"Difficulty: {self.selected_difficulty.name}"
            else:
                text = option
            draw_text(surface, text, 32, self.screen_width // 2, start_y + i * 40, color)


    def _draw_instructions(self, surface):
        """Draw the instructions at the bottom of the screen."""
        draw_text(surface, "Up/Down: Select  -  Left/Right: Adjust  -  Space/Enter: Start", 24, self.screen_width // 2, self.screen_height - 10)


#endregion
################################################################################
#region PauseMenu


class PauseMenu:
    """
    Handles the pause menu of the game.

    Attributes:
        screen_width (int): The width of the screen.
        screen_height (int): The height of the screen.

    Methods:
        handle_input: Handle input events for the pause menu.
        draw: Draw the pause menu on the screen.
    """

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height


    def handle_input(self, event):
        """Handle input events for the pause menu."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return GameState.PLAYING
            elif event.key == pygame.K_q:
                return GameState.MENU
        return GameState.PAUSED


    def draw(self, surface, snake, food):
        """Draw the pause menu on the screen."""
        snake.draw(surface)
        food.draw(surface)
        draw_text(surface, "PAUSED", 64, self.screen_width // 2, self.screen_height // 9)
        draw_text(surface, "ESC - Resume | Q - Quit", 32, self.screen_width // 2, self.screen_height // 2)


#endregion
################################################################################
#region GameOver


class GameOver:
    """
    Handles the game over screen.

    Attributes:
        screen_width (int): The width of the screen.
        screen_height (int): The height of the screen.

    Methods:
        handle_input: Handle input events for the game over screen.
        draw: Draw the game over screen on the screen.
    """

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_high_score = False


    def set_high_score_status(self, is_high_score):
        self.is_high_score = is_high_score


    def handle_input(self, event):
        """Handle input events for the game over screen."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return GameState.MENU
        return GameState.GAME_OVER


# --------------------------------------
# Draw
# --------------------------------------
    def draw(self, surface, score):
        """Draw the game over screen with high scores."""
        self._draw_game_over_text(surface)
        self._draw_high_score_message(surface)
        self._draw_current_score(surface, score)
        self._draw_high_scores(surface, score)
        self._draw_instructions(surface)


    def _draw_game_over_text(self, surface):
        """Draw the game over text on the screen."""
        draw_text(surface, "GAME OVER!", 64, self.screen_width // 2, self.screen_height // 9)


    def _draw_high_score_message(self, surface):
        """Draw the high score message if applicable."""
        if self.is_high_score:
            draw_text(surface, "NEW HIGH SCORE!", 32, self.screen_width // 2, self.screen_height // 4)


    def _draw_current_score(self, surface, score):
        """Draw the current score on the screen."""
        draw_text(surface, f"Your Score: {score.score}", 32, self.screen_width // 2, self.screen_height // 3)


    def _draw_high_scores(self, surface, score):
        """Draw the high scores on the screen."""
        score.high_scores.draw(surface, self.screen_width // 2, self.screen_height // 2.5)


    def _draw_instructions(self, surface):
        """Draw the instructions at the bottom of the screen."""
        draw_text(surface, "Press SPACE to return to Menu", 32, self.screen_width // 2, self.screen_height - 40)
