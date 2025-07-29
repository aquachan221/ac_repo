import os
import msvcrt
import time
import random #type: ignore
import winsound
import sys

melee_classes = ["1: gladiator", "2: bulwark", "3: berserker", "4: shadowblade"]
magic_classes = ["5: pyromancer", "6: chronomancer", "7: illusionist", "8: geomancer", "9: technomancer", "10: runeweaver", "11: stormcaller", "12: voidwalker", "13: soulbinder", "14: bloodmage", "15: arcane_scholar", "16: lightweaver"]
healer_classes = ["17: cleric", "18: druid", "19: shaman", "20: field_surgeon", "21: beastmaster", "22: spiritwalker", "23: zigger", "24: soulhealer", "25: arcane_healer"]
ranged_classes = ["26: archer", "27: marksman", "28: sniper", "29: gunslinger"]
rogue_classes = ["30: rogue", "31: assassin", "32: trickster", "33: bounty_hunter", "34: explorer", "35: scout", "36: survivalist"]
misc_classes= ["37: soulreaper", "38: cosmicherald"]

#silly
gru = """Felonious Gru – Tactical Mastermind, Minion Commander, and Unexpected Family Man
Ah, greetings. I am Gru—former supervillain, expert strategist, and now, a reluctant yet devoted father. My name has been whispered in fear across villainous circles, mostly due to my reputation for audacious heists, unconventional problem-solving, and my unpredictable army of Minions.
At one time, my life revolved around stealing great treasures, crafting elaborate schemes, and perfecting my villainous monologue delivery. My most legendary triumph? Stealing the Moon, an achievement unmatched in history. I held the celestial body in the palm of my hand—until, unfortunately, physics and other annoying factors forced me to return it.

Former Occupation: Supervillain
- Successfully stole the Moon (briefly)
- Attempted to outdo rival supervillain Vector (success is debatable)
- Commanded an entire legion of Minions, a feat requiring near-supernatural patience
- Built a villain lair that was as terrifying as it was highly impractical

Current Status: Anti-Villain League Agent & Full-Time Father
Yes, my grand ambitions for world domination have since been adjusted. I now dedicate my strategic genius to stopping villains even more ridiculous than I once was, thanks to my forced recruitment by the Anti-Villain League.
This has also led to an unexpected partnership with Lucy Wilde, a frustratingly competent AVL agent who, despite all logic, found my personality charming. She is now my wife, meaning that my life remains entirely unpredictable.

The Children: My Greatest (and Most Chaotic) Challenge
My life took an unexpected detour when three small humans entered it—Margo, Edith, and Agnes. At first, their presence was nothing more than a strategic deception to further my villainous goals. But, as fate would have it, I became a father—something even more challenging than orchestrating an international crime spree.
Difficult negotiations now revolve around bedtimes, school events, and an ongoing debate about unicorn ownership.
Despite all of this—despite the absurdity of my situation, the constant chaos, and the fact that my house is never quiet for more than 30 seconds—I find that I would not trade it for anything.

The Minions: My Wildly Unpredictable Army
Ah, the Minions. Small, yellow, excitable beyond comprehension, and utterly chaotic.
While their intelligence is questionable at best, their enthusiasm for destruction is unrivaled. A simple task such as “build a laser” might result in a banana-powered singing device, and an order to clean the lab could somehow burn down an entire kitchen (which was not even part of the lab).
Despite their manic tendencies, they are loyal beyond reason. They have been with me through triumph, failure, and several legally questionable situations that I will not elaborate on.

Top 5 Most Chaotic Minion Incidents
- Accidentally set fire to my kitchen while attempting to toast a single slice of bread
- Created an explosive device while trying to make a birthday cake
- Mistook a top-secret AVL communication device for a karaoke microphone (mission: compromised)
- Hijacked my car to turn it into a submarine (without telling me)
- Managed to launch a Minion into orbit during an experiment gone terribly wrong

Signature Gadgets
🔹 Freeze Ray – My greatest invention. Ideal for stopping enemies… or keeping drinks chilled..
🔹 Shrink Ray – Briefly used to steal the Moon; results varied.
🔹 Despicamobile – Formerly a villainous getaway vehicle, now mostly used for school pickup duty.

My Personal Motto
"Life is full of disappointments. Otherwise, it wouldn’t be life."
Though my days of villainy are behind me, I find that life is still an unpredictable mess, much like my Minions. And frankly, I wouldn’t have it any other way.
Now, if you will excuse me, I must prevent Agnes from attempting to adopt yet another unicorn and ensure that my Minions have not burned down the kitchen again."""

#weird goofy ahh algorith

#variables
#player_name=player_name
#player_gender=player_gender
#player_class=player_class
player_hunger=100
player_health=100
player_mana=100
player_xp=0
player_level=0
#currencies
player_imperial_marks=0
player_hexcoins=0
player_verdant_gems=0
player_obsidian_shards=0
player_emberfragments=0
#guild reputations
player_emberforged_reputation=0
player_shadowveil_reputation=0
player_verdantpact_reputation=0
player_stormcallers_reputation=0
player_ironclad_brotherhood_reputation=0
player_arcane_lexicon_reputation=0
player_silverfang_syndicate_reputation=0
player_gilded_coin_reputation=0
player_hollowborn_reputation=0
player_celestial_vanguard_reputation=0
#secret society reputations
player_cryptic_order_reputation=0
player_veilwalkers_reputation=0


WIDTH, HEIGHT = 65, 15
player_x, player_y = WIDTH // 2, HEIGHT // 2
bot_x, bot_y = 1, 1 
BOT_SPEED = 1
bot_move_counter = 0


walls = [(3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3),
         (9, 3), (10, 3), (11, 3), (12, 3), (13, 3), (14, 3),
         (15, 3), (16, 3), (17, 3), (18, 3), (19, 3), (20, 3),
         (21, 3), (22, 3), (23, 3), (24, 3), (25, 3), (26, 3),
         (27, 3), (28, 3), (29, 3)]

current_map=walls

def slow_print(text, delay=0.05):
	for char in text:
		print(char, end='', flush=True)
		time.sleep(delay)
	print()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def place_wall(x, y):
    """Place a wall at (x, y) if within bounds and not already present."""
    if 0 <= x < WIDTH and 0 <= y < HEIGHT and (x, y) not in walls:
        walls.append((x, y))

def draw():
    for y in range(HEIGHT): 
        row = ""
        for x in range(WIDTH):
            if (x, y) in walls:
                row += "#"
            elif x == player_x and y == player_y:
                row += "A"
            elif x == bot_x and y == bot_y:
                row += "B"
            else:
                row += "."
        print(row)

def move(dx, dy, steps=1):
    global player_x, player_y
    for _ in range(steps):
        nx, ny = player_x + dx, player_y + dy
        if (
            0 <= nx < WIDTH and 0 <= ny < HEIGHT
            and (nx, ny) not in walls
        ):
            player_x, player_y = nx, ny
        else:
            break

def move_bot():
    global bot_x, bot_y
    dx = 1 if bot_x < player_x else -1 if bot_x > player_x else 0
    dy = 1 if bot_y < player_y else -1 if bot_y > player_y else 0

    # Try to move in x direction first, but don't move into player or wall
    if dx != 0 and 0 <= bot_x + dx < WIDTH:
        if not (bot_x + dx == player_x and bot_y == player_y) and (bot_x + dx, bot_y) not in walls:
            bot_x += dx
            return
    # Then try y direction, but don't move into player or wall
    if dy != 0 and 0 <= bot_y + dy < HEIGHT:
        if not (bot_x == player_x and bot_y + dy == player_y) and (bot_x, bot_y + dy) not in walls:
            bot_y += dy
            return

def game_loop():
    global bot_move_counter
    while True:
        print("\033[H", end="")  # ANSI escape: move cursor to top-left
        draw()
        bot_move_counter += 1
        if bot_move_counter >= BOT_SPEED:
            move_bot()
            bot_move_counter = 0
        if msvcrt.kbhit():
            key = msvcrt.getch()
            # Check for Shift+WASD (uppercase letters)
            if key in (b'W', b'S', b'A', b'D'):
                if key == b'W':
                    move(0, -1, steps=2)
                elif key == b'S':
                    move(0, 1, steps=2)
                elif key == b'A':
                    move(-1, 0, steps=4)
                elif key == b'D':
                    move(1, 0, steps=4)
            else:
                key = key.lower()
                if key == b'w':
                    move(0, -1)
                elif key == b's':
                    move(0, 1)
                elif key == b'a':
                    move(-1, 0)
                elif key == b'd':
                    move(1, 0)
                elif key == b'q':
                    break
        time.sleep(0.1)

def charec_create():
    global player_gender
    global player_class
    global name_verify
    # Initialize name_verify to avoid undefined error
    name_verify = ""
    print("Charector creation:")
    while True:
        determ_player_name=input("What is your name? ").strip()
        if len(determ_player_name) >= 17:
            print("hey, unfortunately your name has to be under 17 characters :(")
        elif determ_player_name == "gru":
            print(f"{gru}")
            time.sleep(5)
            start_game()
        else:
            name_verify=input(f"Is {determ_player_name} your name? (yes/no) ").lower()
        if name_verify == "yes":
            determ_player_gender=input("1: female, 2: male")
            player_gender=determ_player_gender
            determ_player_class=input("selecet your class:\n" + "\n".join(melee_classes + magic_classes + healer_classes + ranged_classes + rogue_classes + misc_classes) + "\n")
            player_class=determ_player_class
            game_loop()
        if name_verify == "no":
            charec_create()
        else:
            print("nuh uh")
        charec_create()

def determ_intro():
    intro_num=random.randint(0, 10)

def start_game():
    clear()
    slow_print("Welcome to Aqua Story!")
    main_menu_choice=input("1: continue, 2: load a save, 3: new save, 4: exit\n")
    if main_menu_choice == "1":
        slow_print("loading last played save")
        game_loop()
    if main_menu_choice == "2":
        slow_print(f"select a save file to load:\n1: Save 1\n2: Save 2\n3: Save 3\n4: Save 4\n5: Save 5")
    if main_menu_choice == "3":
        new_save()
    if main_menu_choice == "4":
        slow_print("cj mccreery sucks")
        os._exit(0)
    if main_menu_choice not in ["1", "2", "3", "4"]:
        slow_print("nuh uh")
        start_game()

def new_save():
    clear()
    print("New save created")
    charec_create()

        



"""goofy
place_wall(10, 5)
place_wall(11, 5)
place_wall(12, 5)
place_wall(13, 5)
place_wall(14, 5)
place_wall(20, 10)
place_wall(21, 10)
place_wall(22, 10)
"""

clear()


start_game()