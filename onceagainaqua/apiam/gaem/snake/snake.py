import tkinter as tk
from tkinter import simpledialog
import random

# --- Game Settings ---
CELL_SIZE = 20
DELAY = 100
food_count = 3
WIDTH, HEIGHT = 400, 400

# --- Setup ---
root = tk.Tk()
root.title("Snake Game")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

snake = [(100, 100), (80, 100), (60, 100)]
direction = None
foods = []
game_over = False
game_started = False
high_score = 0
restart_btn = None  # Restart button for canvas

# --- Drawing ---
def draw_segment(x, y, color="green"):
    canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=color, outline="")

def draw_food():
    global foods
    while len(foods) < food_count:
        fx = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        fy = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        new_food = (fx, fy)
        if new_food not in snake and new_food not in foods:
            foods.append(new_food)
    for f in foods:
        draw_segment(f[0], f[1], color="red")

def update():
    global direction, foods, game_over, high_score, restart_btn

    canvas.delete("all")

    if not game_started:
        canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Press any key to begin", fill="white", font=("Helvetica", 16))
        root.after(DELAY, update)
        return

    if game_over:
        canvas.create_text(WIDTH // 2, HEIGHT // 2 - 20, text="Game Over!", fill="white", font=("Helvetica", 24))
        canvas.create_text(WIDTH // 2, HEIGHT // 2 + 20, text=f"High Score: {high_score}", fill="lightgreen", font=("Helvetica", 14))

        if restart_btn is None:
            restart_btn = tk.Button(root, text="Restart Game", font=("Helvetica", 12), command=reset_game)
            restart_btn.place(x=WIDTH // 2 - 50, y=HEIGHT // 2 + 50)
        return

    draw_food()

    head_x, head_y = snake[0]
    if direction == "Right": head_x += CELL_SIZE
    elif direction == "Left": head_x -= CELL_SIZE
    elif direction == "Up": head_y -= CELL_SIZE
    elif direction == "Down": head_y += CELL_SIZE

    new_head = (head_x, head_y)

    if (head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or new_head in snake):
        game_over = True
        high_score = max(high_score, len(snake))
        root.after(DELAY, update)
        return

    snake.insert(0, new_head)

    if new_head in foods:
        foods.remove(new_head)
    else:
        snake.pop()

    for segment in snake:
        draw_segment(segment[0], segment[1])

    root.after(DELAY, update)

# --- Controls ---
def change_dir(event):
    global direction, game_started
    key = event.keysym.lower()
    key_map = {
        "up": "Up", "w": "Up",
        "down": "Down", "s": "Down",
        "left": "Left", "a": "Left",
        "right": "Right", "d": "Right"
    }
    if key in key_map:
        direction = key_map[key]
        if not game_started:
            game_started = True
            update()

# --- Config Dialogs ---
def set_food_count():
    global food_count
    value = simpledialog.askinteger("Food Count", "Number of food items:", minvalue=1, maxvalue=20)
    if value:
        food_count = value
        reset_game()

def set_map_size():
    global WIDTH, HEIGHT, canvas
    new_width = simpledialog.askinteger("Map Width", "Canvas width:", minvalue=100, maxvalue=1000)
    new_height = simpledialog.askinteger("Map Height", "Canvas height:", minvalue=100, maxvalue=1000)
    if new_width and new_height:
        WIDTH, HEIGHT = new_width, new_height
        canvas.config(width=WIDTH, height=HEIGHT)
        reset_game()

# --- Game Reset ---
def reset_game():
    global snake, foods, direction, game_over, game_started, restart_btn
    snake = [(100, 100), (80, 100), (60, 100)]
    foods.clear()
    direction = None
    game_over = False
    game_started = False

    if restart_btn:
        restart_btn.destroy()
        restart_btn = None

    update()

# --- Settings Menu ---
menubar = tk.Menu(root)
settings_menu = tk.Menu(menubar, tearoff=0)
settings_menu.add_command(label="Set Food Count", command=set_food_count)
settings_menu.add_command(label="Set Map Size", command=set_map_size)
menubar.add_cascade(label="Settings", menu=settings_menu)
root.config(menu=menubar)

# --- Start ---
root.bind("<Key>", change_dir)
reset_game()
root.mainloop()