################################################################################
#region Imports


# Standard Library
from pathlib import Path


# Local
from scripts.draw_text import draw_text


#endregion
################################################################################
#region GameScore


class GameScore:
    """
    Handle the game score.

    Attributes:
        score (int): The current score.

    Methods:
        increment: Increment the score by 1.
        reset: Reset the score to 0.
        draw: Draw the score on the screen.

    """

    def __init__(self):
        self.score = 0
        self.high_scores = HighScores()


    def increment(self):
        """Increment the score by 1."""
        self.score += 1


    def reset(self):
        """Reset the score to 0."""
        self.score = 0


    def draw(self, surface, x, y, size=24):
        """Draw the score on the screen."""
        score_text = f"Score: {self.score}"
        draw_text(surface, score_text, size, x, y)


#endregion
################################################################################
#region HighScores


class HighScores:
    """
    High scores class.

    Attributes:
        score_range (int): The number of high scores to display.
        scores (list): The list of high scores.
        scores_file (Path): The file to store the high scores.

    Methods:
        load_scores: Load the high scores from the file.
        save_scores: Save the high scores to the file.
        add_score: Add a new score to the list of high scores.
        draw: Draw the high scores on the screen.

    """

    def __init__(self):
        self.score_range = 5
        self.scores = []
        self.scores_file = Path("high_scores.txt")
        self._load_scores()


# --------------------------------------
# Load
# --------------------------------------
    def _load_scores(self):
        """Load the high scores from the text file."""
        self._fetch_saved_scores()
        self._truncate_and_fill_scores()


    def _truncate_and_fill_scores(self):
        """Truncate the scores to the score range and fill with zeros if needed."""
        self.scores = sorted(self.scores, reverse=True)[:self.score_range]
        while len(self.scores) < self.score_range:
            self.scores.append(0)


    def _fetch_saved_scores(self):
        """Fetch the saved scores from the text file."""
        try:
            if self.scores_file.exists():
                with open(self.scores_file, 'r') as f:
                    self.scores = [int(score.strip()) for score in f.readlines() if score.strip()]
        except:
            self.scores = []


# --------------------------------------
# Save
# --------------------------------------
    def _save_scores(self):
        """Save the high scores to the text file."""
        with open(self.scores_file, 'w') as f:
            for score in self.scores:
                f.write(f"{score}\n")


    def add_score(self, score):
        """Add a new score to the list of high scores."""
        self.scores.append(score)
        self.scores = sorted(self.scores, reverse=True)[:self.score_range]
        self._save_scores()
        return score >= self.scores[-1]  # Return True if high score


# --------------------------------------
# Draw
# --------------------------------------
    def draw(self, surface, x, y, spacing=30):
        """Draw the high scores on the screen."""
        draw_text(surface, "HIGH SCORES", 48, x, y)
        for i, score in enumerate(self.scores, 1):
            draw_text(surface, f"{i}. {score}", 24, x, y + spacing * (i + 1))
