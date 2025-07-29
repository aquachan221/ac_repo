import curses
import random#type: ignore

MAP_WIDTH = 50
MAP_HEIGHT = 30
PLAYER_SYMBOL = "@"
ENEMY_SYMBOL = "E"
FLOOR_SYMBOL = "."
WALL_SYMBOL = "#"

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 10
        self.weapon = {"name": "Sword", "damage": 2, "range": 1}  # Basic sword

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 5  # Enemy HP

def generate_map():
    """Generate a simple dungeon"""
    game_map = [[FLOOR_SYMBOL for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

    # Create borders
    for x in range(MAP_WIDTH):
        game_map[0][x] = WALL_SYMBOL
        game_map[MAP_HEIGHT - 1][x] = WALL_SYMBOL
    for y in range(MAP_HEIGHT):
        game_map[y][0] = WALL_SYMBOL
        game_map[y][MAP_WIDTH - 1] = WALL_SYMBOL
    
    # Place random walls
    for _ in range(50):  
        x, y = random.randint(1, MAP_WIDTH - 2), random.randint(1, MAP_HEIGHT - 2)
        game_map[y][x] = WALL_SYMBOL

    return game_map

def attack_enemy(player, enemy):
    """Handles attacking an enemy when within range"""
    distance = abs(player.x - enemy.x) + abs(player.y - enemy.y)
    if distance <= player.weapon["range"]:  # Check attack range
        enemy.health -= player.weapon["damage"]
        return f"You hit the {ENEMY_SYMBOL} with your {player.weapon['name']}! (-{player.weapon['damage']} HP)"
    return "No enemy in range to attack!"

def main(stdscr):
    """Main game loop"""
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input
    stdscr.timeout(100)  # Refresh every 100ms

    # Enable colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)  # Red for health
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # White for standard text

    game_map = generate_map()
    player = Player(2, 2)
    enemy = Enemy(MAP_WIDTH - 5, MAP_HEIGHT - 5)
    attack_message = ""  # Stores attack feedback

    while player.health > 0:
        stdscr.clear()

        # Draw map
        for y, row in enumerate(game_map):
            stdscr.addstr(y, 0, "".join(row))

        # Draw player and enemy
        stdscr.addch(player.y, player.x, PLAYER_SYMBOL)
        if enemy.health > 0:
            stdscr.addch(enemy.y, enemy.x, ENEMY_SYMBOL)

        # Get player input
        key = stdscr.getch()
        new_x, new_y = player.x, player.y

        if key in [curses.KEY_UP, ord("w")]: new_y -= 1
        if key in [curses.KEY_DOWN, ord("s")]: new_y += 1
        if key in [curses.KEY_LEFT, ord("a")]: new_x -= 1
        if key in [curses.KEY_RIGHT, ord("d")]: new_x += 1

        # Check for collisions
        if game_map[new_y][new_x] != WALL_SYMBOL:
            player.x, player.y = new_x, new_y

        # Enemy random movement
        if enemy.health > 0:
            enemy.x += random.choice([-1, 0, 1])
            enemy.y += random.choice([-1, 0, 1])
            enemy.x = max(1, min(MAP_WIDTH - 2, enemy.x))
            enemy.y = max(1, min(MAP_HEIGHT - 2, enemy.y))

        # Combat check
        if player.x == enemy.x and player.y == enemy.y:
            player.health -= 1

        # Attack system
        if key == ord(" "):  # Press SPACE to attack
            attack_message = attack_enemy(player, enemy)

        # Ensure attack_message fits within terminal limits
        attack_message = attack_message[:50]  

        # Draw separator line
        stdscr.addstr(MAP_HEIGHT, 0, "-" * MAP_WIDTH)

        # Catch any curses errors to prevent crashes
        try:
            stdscr.attron(curses.color_pair(2))  # White text for attack message
            stdscr.addstr(MAP_HEIGHT + 1, 0, attack_message)
            stdscr.attroff(curses.color_pair(2))

            stdscr.attron(curses.color_pair(1))  # Red text for health bar
            stdscr.addstr(MAP_HEIGHT + 2, 0, f"Player HP: {player.health} | Enemy HP: {enemy.health if enemy.health > 0 else 'DEAD'}")
            stdscr.attroff(curses.color_pair(1))
        except curses.error:
            pass  # Ignore printing errors if screen is too small

        stdscr.refresh()

curses.wrapper(main)