import pygame # type: ignore
import sys
import random # type: ignore

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Snake and food
def random_position():
    x = random.randrange(0, WIDTH, CELL_SIZE)
    y = random.randrange(0, HEIGHT, CELL_SIZE)
    return (x, y)

snake = [random_position()]
direction = (CELL_SIZE, 0)
food = random_position()
score = 0
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def draw_snake(snake):
    for pos in snake:
        pygame.draw.rect(screen, GREEN, (*pos, CELL_SIZE, CELL_SIZE))

def draw_food(pos):
    pygame.draw.rect(screen, RED, (*pos, CELL_SIZE, CELL_SIZE))

def show_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def game_over():
    text = font.render("Game Over!", True, RED)
    screen.blit(text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)

    # Move snake
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake):
        game_over()

    snake.insert(0, new_head)
    if new_head == food:
        score += 1
        while True:
            food = random_position()
            if food not in snake:
                break
    else:
        snake.pop()

    # Draw everything
    screen.fill(BLACK)
    draw_snake(snake)
    draw_food(food)
    show_score(score)
    pygame.display.flip()
    clock.tick(10)