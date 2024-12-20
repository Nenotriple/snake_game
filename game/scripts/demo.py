################################################################################
#region Imports


# Standard Library
from collections import deque


# Local
from scripts.collision_detection import CollisionDetection
from scripts.snake import Snake
from scripts.food import Food


from collections import deque
from scripts.constants import UP, DOWN, LEFT, RIGHT, GRID_WIDTH, GRID_HEIGHT


#endregion
################################################################################
#region Pathfinding


class Pathfinding:
    """
    Class to handle pathfinding for the snake.

    Attributes:
        snake (Snake): The snake object.
        collision_detector (CollisionDetection): The collision detector object.

    Methods:
        _is_valid_move: Check if a position is within the grid and not part of the snake.
        _flood_fill: Count the number of accessible cells from a starting position.
        _bfs: Breadth-first search to find the shortest path to the goal.
        _get_safe_direction: Find the direction with the largest accessible space.
        get_next_direction: Calculate the next direction for the snake to move.
    """

    def __init__(self, snake, collision_detector):
        self.snake = snake
        self.collision_detector = collision_detector


    def _is_valid_move(self, position):
        """Check if a position is within the grid and not part of the snake."""
        x, y = position
        return (0 <= x < GRID_WIDTH and
                0 <= y < GRID_HEIGHT and
                position not in self.snake.body)


    def _flood_fill(self, start):
        """Count the number of accessible cells from a starting position."""
        queue = deque([start])
        visited = set([start])
        while queue:
            current = queue.popleft()
            for direction in [UP, DOWN, LEFT, RIGHT]:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if neighbor not in visited and self._is_valid_move(neighbor):
                    visited.add(neighbor)
                    queue.append(neighbor)
        return len(visited)


    def _bfs(self, start, goal):
        """Breadth-first search to find the shortest path to the goal."""
        queue = deque([(start, [])])
        visited = set([start])
        while queue:
            current, path = queue.popleft()
            if current == goal:
                return path
            for direction in [UP, DOWN, LEFT, RIGHT]:
                new_position = (current[0] + direction[0], current[1] + direction[1])
                if new_position not in visited and self._is_valid_move(new_position):
                    visited.add(new_position)
                    queue.append((new_position, path + [direction]))
        return []


    def _get_safe_direction(self, head):
        """Find the direction with the largest accessible space."""
        safe_moves = []
        for direction in [UP, DOWN, LEFT, RIGHT]:
            next_position = (head[0] + direction[0], head[1] + direction[1])
            if self._is_valid_move(next_position):
                space = self._flood_fill(next_position)
                safe_moves.append((space, direction))
        return max(safe_moves)[1] if safe_moves else None


    def get_next_direction(self, food_position):
        """Calculate the next direction for the snake to move."""
        head = self.snake.body[0]
        path_to_food = self._bfs(head, food_position)
        # If path to food is safe, follow it
        if path_to_food:
            next_position = (head[0] + path_to_food[0][0], head[1] + path_to_food[0][1])
            if self._flood_fill(next_position) > len(self.snake.body):
                return path_to_food[0]
        # If path to food is not safe, follow tail or choose a safe direction
        tail = self.snake.body[-1]
        path_to_tail = self._bfs(head, tail)
        if path_to_tail:
            return path_to_tail[0]
        # If no path to tail, choose a safe direction
        return self._get_safe_direction(head)


#endregion
################################################################################
#region DemoGame


class DemoGame:
    """
    The demo game class to handle the game logic.

    Attributes:
        snake (Snake): The snake object.
        food (Food): The food object.
        collision_detector (CollisionDetection): The collision detector object.
        navigation_handler (Pathfinding): The pathfinding object.
        score (Score): The score object.

    Methods:
        update_theme: Update the theme of the snake and food.
        update: Update the game state.
        handle_collisions: Handle collisions with the wall, self, and food.
        navigate_towards_food: Move the snake towards the food.
        draw: Draw the snake and food on the surface.
    """

    def __init__(self, theme, score):
        self.snake = Snake(theme)
        self.food = Food(theme, self.snake)
        self.collision_detector = CollisionDetection(GRID_WIDTH, GRID_HEIGHT)
        self.navigation_handler = Pathfinding(self.snake, self.collision_detector)
        self.score = score
        self.update_theme(theme)


    def update_theme(self, theme):
        """Update the theme of the snake and food."""
        self.snake.theme = theme
        self.food.theme = theme


    def update(self):
        """Update the game state."""
        self.navigate_towards_food()
        self.snake.move()
        head = self.snake.body[0]
        self.handle_collisions(head)


    def handle_collisions(self, head):
        """Handle collisions with the wall, self, and food."""
        # if food
        if self.collision_detector.check_food_collision(head, self.food.position):
            self.snake.grow()
            self.score.increment()
            self.food.position = self.food.random_position(self.snake)
        # if wall or self
        if (self.collision_detector.check_wall_collision(head) or
            self.collision_detector.check_self_collision(self.snake)):
            self.snake = Snake(self.snake.theme)
            self.food = Food(self.food.theme, self.snake)
            self.navigation_handler = Pathfinding(self.snake, self.collision_detector)
            self.score.reset()


    def navigate_towards_food(self):
        """Move the snake towards the food."""
        next_direction = self.navigation_handler.get_next_direction(self.food.position)
        if next_direction:
            self.snake.direction = next_direction


    def draw(self, surface):
        """Draw the snake and food on the surface."""
        self.snake.draw(surface)
        self.food.draw(surface)
