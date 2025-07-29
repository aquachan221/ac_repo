import random#type: ignore
class Zombie:
    def __init__(self, x, y, speed=1, color=(0, 200, 0)):
        """Initialize zombie with position, speed, and color."""
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color

    def move_toward(self, target_x, target_y):
        """Basic AI: Move toward the target (player)."""
        if self.x < target_x:
            self.x += min(self.speed, target_x - self.x)  # Move right
        elif self.x > target_x:
            self.x -= min(self.speed, self.x - target_x)  # Move left
        
        if self.y < target_y:
            self.y += min(self.speed, target_y - self.y)  # Move down
        elif self.y > target_y:
            self.y -= min(self.speed, self.y - target_y)  # Move up

    def randomize_position(self, grid_width, grid_height):
        """Set zombie to a random position in the grid."""
        self.x = random.randint(0, grid_width - 1)
        self.y = random.randint(0, grid_height - 1)

    def draw(self, screen, grid_size):
        """Draw zombie on the screen."""
        import pygame
        zombie_rect = pygame.Rect(self.x * grid_size, self.y * grid_size, grid_size, grid_size)
        pygame.draw.rect(screen, self.color, zombie_rect)

    def get_position(self):
        """Return zombie's current position."""
        return self.x, self.y