import tkinter as tk
import random
import os

# --- Setup ---
root = tk.Tk()
root.title("Blackjack")

deck = [("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6),
        ("7", 7), ("8", 8), ("9", 9), ("10", 10),
        ("J", 10), ("Q", 10), ("K", 10), ("A", 11)] * 4

player_hand = []
dealer_hand = []

card_images = {}

# --- Load images ---
def load_images():
    for name, _ in deck:
        path = os.path.join("cards", f"{name}.png")
        card_images[name] = tk.PhotoImage(file=path)

# --- Game Logic ---
def draw_card():
    return random.choice(deck)

def calculate_score(hand):
    score = sum(card[1] for card in hand)
    aces = sum(1 for card in hand if card[0] == "A")
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

def reset_game():
    global player_hand, dealer_hand
    player_hand = [draw_card(), draw_card()]
    dealer_hand = [draw_card(), draw_card()]
    update_ui()

def hit():
    player_hand.append(draw_card())
    update_ui()
    if calculate_score(player_hand) > 21:
        status_label.config(text="Bust! Dealer wins.")

def stand():
    while calculate_score(dealer_hand) < 17:
        dealer_hand.append(draw_card())
    update_ui()
    decide_winner()

def decide_winner():
    p_score = calculate_score(player_hand)
    d_score = calculate_score(dealer_hand)
    if d_score > 21 or p_score > d_score:
        status_label.config(text="Player wins!")
    elif p_score == d_score:
        status_label.config(text="Push!")
    else:
        status_label.config(text="Dealer wins.")

def update_ui():
    for widget in player_frame.winfo_children():
        widget.destroy()
    for widget in dealer_frame.winfo_children():
        widget.destroy()

    for card in player_hand:
        img = card_images[card[0]]
        label = tk.Label(player_frame, image=img)
        label.pack(side="left")

    for card in dealer_hand:
        img = card_images[card[0]]
        label = tk.Label(dealer_frame, image=img)
        label.pack(side="left")

    score_label.config(text=f"Score: {calculate_score(player_hand)}")

# --- GUI Layout ---
load_images()

dealer_frame = tk.Frame(root)
dealer_frame.pack()
tk.Label(dealer_frame, text="Dealer", font=("Helvetica", 14)).pack(side="top")

player_frame = tk.Frame(root)
player_frame.pack()
tk.Label(player_frame, text="Player", font=("Helvetica", 14)).pack(side="top")

score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 12))
score_label.pack()

status_label = tk.Label(root, text="", font=("Helvetica", 16), fg="blue")
status_label.pack()

tk.Button(root, text="Hit", command=hit).pack(side="left", padx=10)
tk.Button(root, text="Stand", command=stand).pack(side="left", padx=10)
tk.Button(root, text="Restart", command=reset_game).pack(side="left", padx=10)

reset_game()
root.mainloop()