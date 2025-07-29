import random # type: ignore
import os
import sys
import time

WIDTH, HEIGHT = 20, 10
snake = [(WIDTH // 2, HEIGHT // 2)]
direction = (1, 0)
food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
score = 0

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board():
    clear()
    print(f"Score: {score}")
    for y in range(HEIGHT):
        row = ""
        for x in range(WIDTH):
            if (x, y) == snake[0]:
                row += "O"
            elif (x, y) in snake[1:]:
                row += "o"
            elif (x, y) == food:
                row += "*"
            else:
                row += "."
        print(row)
    print("Use W/A/S/D then Enter to move. Ctrl+C to quit.")

def get_input():
    move = input().lower()
    if move == "w":
        return (0, -1)
    elif move == "s":
        return (0, 1)
    elif move == "a":
        return (-1, 0)
    elif move == "d":
        return (1, 0)
    return None

while True:
    print_board()
    new_dir = get_input()
    if new_dir:
        # Prevent snake from reversing
        if (new_dir[0] != -direction[0] or new_dir[1] != -direction[1]):
            direction = new_dir
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    # Check for collision with walls or self
    if (head[0] < 0 or head[0] >= WIDTH or
        head[1] < 0 or head[1] >= HEIGHT or
        head in snake):
        print_board()
        print("Game Over!")
        break

    snake.insert(0, head)
    if head == food:
        score += 1
        while True:
            food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
            if food not in snake:
                break
    else:
        snake.pop()