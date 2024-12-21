class CollisionDetection:
    """
    Handle the games collision detection.

    Attributes:
        grid_width: The width of the grid.
        grid_height: The height of the grid.

    Methods:
        check_wall_collision: Check if the position is outside the grid.
        check_self_collision: Check if the snake has collided with itself.
        check_food_collision: Check if the snake has collided with the food.
    """

    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height


    def check_wall_collision(self, position, peaceful_mode=False):
        """Check if position collides with walls."""
        x, y = position
        if peaceful_mode:
            return False
        return (x < 0 or x >= self.grid_width or
                y < 0 or y >= self.grid_height)


    def wrap_position(self, position):
        """Wrap position around screen edges."""
        x, y = position
        x = x % self.grid_width
        y = y % self.grid_height
        return (x, y)


    def check_self_collision(self, snake, peaceful_mode=False):
        """Check if snake collides with itself."""
        if peaceful_mode:
            return False
        head = snake.body[0]
        return head in snake.body[1:]


    def check_food_collision(self, head, food_pos):
        """Check if snake head collides with food."""
        return head == food_pos
