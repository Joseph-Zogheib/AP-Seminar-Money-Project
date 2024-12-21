import tkinter as tk
import random
import time

# --- Game Setup ---
WIDTH = 800
HEIGHT = 600
PLAYER_RADIUS = 20
MONEY_RADIUS = 10
NUM_MONEY_SPAWNS = 10  # Number of money objects to spawn

# --- Functions ---
def start_game():
    global is_rich, money_amount, start_time, money_objects
    menu_frame.pack_forget()  # Hide the menu
    game_frame.pack()  # Show the game canvas
    is_rich = random.random() < 0.1  # 10% chance of being rich
    money_amount = 10000 if is_rich else 0
    start_time = time.time()
    money_objects = []
    create_money(NUM_MONEY_SPAWNS)  # Spawn initial money objects
    update_game()

def create_money(num_money):
    global money_objects, money_value
    for _ in range(num_money):
        money_x = random.randint(MONEY_RADIUS, WIDTH - MONEY_RADIUS)
        money_y = random.randint(MONEY_RADIUS, HEIGHT - MONEY_RADIUS)
        money_value = 100 if is_rich else 5
        money = game_canvas.create_oval(
            money_x - MONEY_RADIUS,
            money_y - MONEY_RADIUS,
            money_x + MONEY_RADIUS,
            money_y + MONEY_RADIUS,
            fill="gold",
        )
        money_objects.append(money)

def update_game():
    global money_amount
    elapsed_time = time.time() - start_time
    if elapsed_time >= 60:  # Game ends after 60 seconds
        game_over()
        return

    player_coords = game_canvas.coords(player)

    # Check for collision with all money objects
    for money_id in money_objects:
        money_coords = game_canvas.coords(money_id)
        if (
            player_coords[0] < money_coords[2]
            and player_coords[2] > money_coords[0]
            and player_coords[1] < money_coords[3]
            and player_coords[3] > player_coords[1]
        ):
            money_amount += money_value
            game_canvas.delete(money_id)
            money_objects.remove(money_id)  # Remove collected money from the list
            create_money(1)  # Respawn one money object

    game_canvas.itemconfig(score_text, text=f"Money: ${money_amount}")
    game_canvas.itemconfig(status_text, text=f"Status: {'Rich' if is_rich else 'Poor'}")
    game_canvas.itemconfig(time_text, text=f"Time: {60 - int(elapsed_time)}")
    game_canvas.after(100, update_game)  # Update every 100ms

def game_over():
    game_frame.pack_forget()
    game_over_frame.pack()
    game_over_label.config(text=f"Game Over!\nYou collected ${money_amount}")

def move_player(event):
    x, y = event.x, event.y
    game_canvas.coords(
        player,
        x - PLAYER_RADIUS,
        y - PLAYER_RADIUS,
        x + PLAYER_RADIUS,
        y + PLAYER_RADIUS,
    )

# --- Key Bindings ---
def move_player_keys(event):
    x, y = game_canvas.coords(player)
    speed = 5
    if event.keysym == "Up":
        y -= speed
    elif event.keysym == "Down":
        y += speed
    elif event.keysym == "Left":
        x -= speed
    elif event.keysym == "Right":
        x += speed
    elif event.char == "w":
        y -= speed
    elif event.char == "s":
        y += speed
    elif event.char == "a":
        x -= speed
    elif event.char == "d":
        x += speed
    game_canvas.coords(player, x, y, x + 2 * PLAYER_RADIUS, y + 2 * PLAYER_RADIUS)

# --- UI Setup ---
root = tk.Tk()
root.title("The Money Project Game")

menu_frame = tk.Frame(root)
menu_frame.pack()
tk.Label(menu_frame, text="The Money Project Game", font=("Arial", 24)).pack(pady=20)
tk.Button(menu_frame, text="Play", command=start_game).pack()

game_frame = tk.Frame(root)
game_canvas = tk.Canvas(game_frame, width=WIDTH, height=HEIGHT, bg="lightblue")
game_canvas.pack()
player = game_canvas.create_oval(
    WIDTH / 2 - PLAYER_RADIUS,
    HEIGHT / 2 - PLAYER_RADIUS,
    WIDTH / 2 + PLAYER_RADIUS,
    HEIGHT / 2 + PLAYER_RADIUS,
    fill="blue",
)
score_text = game_canvas.create_text(
    10, 10, anchor="nw", text="Money: $0", font=("Arial", 16)
)
time_text = game_canvas.create_text(
    710, 10, anchor="nw", text="Time: 0", font=("Arial", 16)
)
status_text = game_canvas.create_text(
    10, 35, anchor="nw", text="Status: ", font=("Arial", 12)
)
game_canvas.bind("<Motion>", move_player)
game_canvas.bind("<KeyPress-Up>", move_player_keys)
game_canvas.bind("<KeyPress-Down>", move_player_keys)
game_canvas.bind("<KeyPress-Left>", move_player_keys)
game_canvas.bind("<KeyPress-Right>", move_player_keys)
game_canvas.bind("<KeyPress-w>", move_player_keys)
game_canvas.bind("<KeyPress-s>", move_player_keys)
game_canvas.bind("<KeyPress-a>", move_player_keys)
game_canvas.bind("<KeyPress-d>", move_player_keys)

game_over_frame = tk.Frame(root)
game_over_label = tk.Label(game_over_frame, text="", font=("Arial", 24))
game_over_label.pack(pady=20)

root.mainloop()