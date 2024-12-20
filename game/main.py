"""A simple and efficient Snake game using Pygame."""


################################################################################
#region Imports


# Third Party
import pygame


# Local
from scripts.constants import *
from scripts.food import Food
from scripts.theme import Theme
from scripts.snake import Snake
from scripts.demo import DemoGame, Pathfinding
from scripts.draw_text import draw_text
from scripts.game_score import GameScore
from scripts.collision_detection import CollisionDetection
from scripts.gamestate import GameState, Difficulty, MainMenu, PlayingGame, PauseMenu, GameOver, GameMode
from scripts.sound_manager import SoundManager


#endregion
################################################################################
#region Setup


# Initialize Pygame
pygame.init()


# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()


#endregion
################################################################################
#region MainGame


class MainGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.themes = Theme.get_themes()
        self.current_theme_index = 0
        self.current_theme = self.themes[self.current_theme_index]
        self.score = GameScore()
        self.demo_game = DemoGame(self.current_theme, score=self.score)
        self.base_fps = BASE_FPS
        self.game_speed_string = f"Speed: +0%"
        self.difficulty = Difficulty.MEDIUM
        self.sound_manager = SoundManager()
        self.sound_manager.start_music()
        self.autopilot_enabled = False
        self.navigation_handler = None
        self.playing_game = None
        self.game_mode = GameMode.CLASSIC
        self.initialize_game()


    def initialize_game(self):
        self.current_theme = self.themes[self.current_theme_index]
        self.snake = Snake(self.current_theme)
        self.food = Food(self.current_theme, self.snake)
        self.collision_detector = CollisionDetection(GRID_WIDTH, GRID_HEIGHT)
        self.menu = MainMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.menu.selected_theme_index = self.current_theme_index
        self.pause_menu = PauseMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.game_over = GameOver(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.current_state = GameState.MENU
        self.demo_game = DemoGame(self.current_theme, score=self.score)
        self.score.reset()
        self.navigation_handler = Pathfinding(self.snake, self.collision_detector)
        self.autopilot_enabled = False
        self.playing_game = PlayingGame(self.snake, self.food, self.collision_detector, self.score)
        self.playing_game.set_game_mode(self.game_mode)
        self.playing_game.set_navigation_handler(self.navigation_handler)


# --------------------------------------
# Input
# --------------------------------------
    def handle_input_events(self):
        """
        Handle input events.

        Returns:
            bool: True if the game should continue running, False if the game should exit.

        Call this method once per frame to handle input events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.sound_manager.stop_music()
                return False
            if event.type == pygame.USEREVENT + 1:  # Music end event
                self.sound_manager.handle_music_end()
            if self.current_state == GameState.MENU:
                self.handle_main_menu_input(event)
            elif self.current_state == GameState.PLAYING:
                self.handle_game_movement_input(event)
            elif self.current_state == GameState.PAUSED:
                self.handle_pause_menu_input(event)
            elif self.current_state == GameState.GAME_OVER:
                self.handle_game_over_input(event)
        return True


    def handle_main_menu_input(self, event):
        new_state, theme_index, difficulty = self.menu.handle_input(event)
        if new_state is None:  # Game was exited
            return
        if theme_index != self.current_theme_index:
            self.current_theme_index = theme_index
            self.current_theme = self.themes[self.current_theme_index]
            self.demo_game.update_theme(self.current_theme)
        if difficulty != self.difficulty:
            self.difficulty = difficulty
        if new_state != self.current_state:
            self.game_mode = self.menu.selected_mode
            self.initialize_game()
        self.current_state = new_state


    def handle_game_movement_input(self, event):
        new_state = self.playing_game.handle_input(event)
        if new_state != self.current_state:
            self.current_state = new_state


    def handle_pause_menu_input(self, event):
        new_state = self.pause_menu.handle_input(event)
        if new_state != self.current_state:
            if new_state == GameState.MENU:
                self.initialize_game()
            self.current_state = new_state


    def handle_game_over_input(self, event):
        new_state = self.game_over.handle_input(event)
        if new_state != self.current_state:
            self.initialize_game()
            self.current_state = new_state


# --------------------------------------
# Update
# --------------------------------------
    def update_game(self):
        """
        Update the game state.

        Call this method once per frame to update the game state and logic.
        """
        if self.current_state == GameState.MENU:
            self.demo_game.update()
        elif self.current_state == GameState.PLAYING:
            self.handle_game_logic()


    def handle_game_logic(self):
        new_state = self.playing_game.update()
        if new_state == GameState.GAME_OVER:
            is_high_score = self.score.high_scores.add_score(self.score.score)
            self.game_over.set_high_score_status(is_high_score)
            self.current_state = GameState.GAME_OVER


# --------------------------------------
# Render
# --------------------------------------
    def render(self):
        """
        Render the game visuals.

        Call this method once per frame to render the game visuals.
        """
        self.draw_game_display()
        self.draw_game_speed()
        self.draw_current_state()
        pygame.display.flip()


    def draw_game_speed(self):
        draw_text(self.screen, self.game_speed_string, 24, SCREEN_WIDTH - 75, BORDER_THICKNESS // 2)


    def draw_game_display(self):
        self.screen.fill(self.current_theme.background_color)
        self.draw_screen_border()
        self.score.draw(self.screen, 50, BORDER_THICKNESS // 2)


    def draw_screen_border(self):
        # Top, Bottom, Left, Right
        pygame.draw.rect(self.screen, self.current_theme.border_color, pygame.Rect(0, 0, SCREEN_WIDTH, BORDER_THICKNESS))
        pygame.draw.rect(self.screen, self.current_theme.border_color, pygame.Rect(0, SCREEN_HEIGHT - BORDER_THICKNESS, SCREEN_WIDTH, BORDER_THICKNESS))
        pygame.draw.rect(self.screen, self.current_theme.border_color, pygame.Rect(0, 0, BORDER_THICKNESS, SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, self.current_theme.border_color, pygame.Rect(SCREEN_WIDTH - BORDER_THICKNESS, 0, BORDER_THICKNESS, SCREEN_HEIGHT))


    def draw_current_state(self):
        if self.current_state == GameState.MENU:
            self.demo_game.draw(self.screen)
            self.menu.draw(self.screen)
        elif self.current_state == GameState.PLAYING:
            self.playing_game.draw(self.screen)
        elif self.current_state == GameState.PAUSED:
            self.pause_menu.draw(self.screen, self.snake, self.food)
        elif self.current_state == GameState.GAME_OVER:
            self.game_over.draw(self.screen, self.score)


#endregion
################################################################################
#region gameloop


    def get_current_speed(self):
        points_per_change = 1
        speed_increase_percent = self.difficulty.value
        score = self.score.score
        speed_multiplier = 1 + (score // points_per_change) * speed_increase_percent
        self.game_speed_string = f"Speed: +{int((speed_multiplier - 1) * 100)}%"
        return int(self.base_fps * speed_multiplier)


    def gameloop(self):
        running = True
        while running:
            running = self.handle_input_events()
            self.update_game()
            self.render()
            self.clock.tick(self.get_current_speed())


#endregion
################################################################################
#region Main


def main():
    game = MainGame()
    game.gameloop()
    pygame.quit()


if __name__ == "__main__":
    main()


#endregion
