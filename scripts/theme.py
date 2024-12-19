from scripts.constants import WHITE, BLACK, YELLOW, RED, GREEN, MAGENTA, LIGHT_BLUE


class Theme:
    """
    The game theme class.

    Colors are represented as RGB tuples.

    Attributes:
        name (str): The name of the theme.
        background_color (tuple): The background color.
        snake_color (tuple): The snake color.
        food_color (tuple): The food color.
        text_color (tuple): The text color.
        border_color (tuple): The border color.
        head_color (tuple): The head color.
        body_color (tuple): The body color.
        tail_color (tuple): The tail color.

    Methods:
        get_themes: Return a list of predefined themes.
    """
    def __init__(self, name=None, background=None, snake=None, food=None, text=None, border=None, head=None, body=None, tail=None):
        self.name = name
        self.background_color = background
        self.snake_color = snake
        self.food_color = food
        self.text_color = text
        self.border_color = border
        self.head_color = head if head else snake
        self.body_color = body if body else snake
        self.tail_color = tail if tail else snake


    @staticmethod
    def get_themes():
        """Return a list of predefined themes."""
        return [
            Theme(
                name=       "Dark",
                background= (30, 30, 30),
                snake=      GREEN,
                food=       RED,
                text=       WHITE,
                border=     (60, 60, 60),
                head=       (0, 200, 0),
                body=       GREEN,
                tail=       (0, 150, 0),
            ),
            Theme(
                name=       "Nokia-1",
                background= (199, 204, 190),
                snake=      (71, 84, 62),
                food=       (71, 84, 62),
                text=       WHITE,
                border=     (50, 60, 40),
                head=       (50, 60, 40),
                body=       (71, 84, 62),
                tail=       (100, 110, 90),
            ),
            Theme(
                name=       "Nokia-2",
                background= (180, 189, 173),
                snake=      (80, 90, 70),
                food=       (80, 90, 70),
                text=       WHITE,
                border=     (60, 70, 50),
                head=       (50, 60, 40),
                body=       (80, 90, 70),
                tail=       (110, 120, 100),
            ),
            Theme(
                name=       "GameBoy",
                background= (155, 188, 15),
                snake=      (48, 98, 48),
                food=       (15, 56, 15),
                text=       WHITE,
                border=     (111, 145, 27),
                head=       (48, 98, 48),
                body=       (75, 139, 72),
                tail=       (111, 145, 27),
            ),
            Theme(
                name=       "2-Bit",
                background= BLACK,
                snake=      WHITE,
                food=       WHITE,
                text=       WHITE,
                border=     WHITE,
                head=       WHITE,
                body=       WHITE,
                tail=       (200, 200, 200),
            ),
            Theme(
                name=       "Pink",
                background= (255, 192, 203),
                snake=      (255, 20, 147),
                food=       (255, 105, 180),
                text=       WHITE,
                border=     (255, 20, 147),
                head=       (255, 0, 127),
                body=       (255, 20, 147),
                tail=       (255, 105, 180),
            ),
            Theme(
                name=       "Neon",
                background= (10, 10, 10),
                snake=      (57, 255, 20),
                food=       MAGENTA,
                text=       WHITE,
                border=     (30, 30, 30),
                head=       (127, 255, 0),
                body=       (57, 255, 20),
                tail=       (0, 255, 100),
            ),
            Theme(
                name=       "Desert",
                background= (233, 221, 199),
                snake=      (181, 101, 29),
                food=       (214, 133, 74),
                text=       WHITE,
                border=     (204, 153, 102),
                head=       (153, 102, 51),
                body=       (181, 101, 29),
                tail=       (214, 133, 74),
            ),
            Theme(
                name=       "Autumn",
                background= (255, 239, 213),
                snake=      (210, 105, 30),
                food=       (255, 69, 0),
                text=       WHITE,
                border=     (139, 69, 19),
                head=       (165, 42, 42),
                body=       (210, 105, 30),
                tail=       (244, 164, 96),
            ),
            Theme(
                name=       "Cyberpunk",
                background= (10, 10, 35),
                snake=      LIGHT_BLUE,
                food=       MAGENTA,
                text=       WHITE,
                border=     (30, 30, 60),
                head=       (0, 200, 200),
                body=       LIGHT_BLUE,
                tail=       (0, 150, 150),
            ),
            Theme(
                name=       "Arcade",
                background= (10, 10, 20),
                snake=      (255, 165, 0),
                food=       YELLOW,
                text=       WHITE,
                border=     MAGENTA,
                head=       (255, 69, 0),
                body=       (255, 165, 0),
                tail=       (255, 140, 0),
            ),
        ]
