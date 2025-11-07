import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import date
import winsound

# ---- CONFIG ----
GOAL_LITRES = 4.0           # Daily goal (L)
CUP_SIZE = 0.25             # Each cup = 250ml
DATA_FILE = "habits.json"


# ---- LOAD & SAVE ----
def load_data():
    """Load or initialize tracking data."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {"water_intake": 0.0, "last_date": str(date.today())}

    # Reset if it's a new day
    if data.get("last_date") != str(date.today()):
        data["water_intake"] = 0.0
        data["last_date"] = str(date.today())

    return data


def save_data():
    """Save progress to file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ---- INIT ----
data = load_data()


# ---- GUI ----
root = tk.Tk()
root.title("Water Tracker")
root.geometry("400x300")
root.configure(bg="#1e1e1e")

goal_label = tk.Label(
    root, text=f"Daily Goal: {GOAL_LITRES} L",
    font=("Arial", 14), fg="white", bg="#1e1e1e"
)
goal_label.pack(pady=10)

bar_canvas = tk.Canvas(root, width=300, height=30, bg="#333", highlightthickness=0)
bar_canvas.pack(pady=10)

water_label = tk.Label(
    root, text="", font=("Arial", 12),
    fg="white", bg="#1e1e1e"
)
water_label.pack(pady=5)


# ---- FUNCTIONS ----
def update_bar():
    """Update the progress bar display."""
    bar_canvas.delete("all")
    ratio = min(data["water_intake"] / GOAL_LITRES, 1.0)
    fill_width = int(300 * ratio)

    # Draw gradient bar (blue shades)
    for i in range(fill_width):
        shade = int(255 * (1 - i / fill_width)) if fill_width else 255
        color = f'#{shade:02x}00ff'
        bar_canvas.create_line(i, 0, i, 30, fill=color)

    water_label.config(text=f"Current: {data['water_intake']:.2f} L / {GOAL_LITRES} L")

    # Goal reached
    if data["water_intake"] >= GOAL_LITRES:
        winsound.PlaySound("2.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        messagebox.showinfo("Nice job!", "You've hit your daily water goal! Resetting for the next round.")
        data["water_intake"] = 0.0
        data["last_date"] = str(date.today())
        save_data()
        update_bar()


def add_water():
    """Add one cup of water and update UI."""
    winsound.PlaySound("2.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
    data["water_intake"] += CUP_SIZE
    save_data()
    update_bar()


# ---- BUTTON ----
add_btn = tk.Button(
    root, text="Add a Cup (250ml)",
    font=("Arial", 12, "bold"),
    bg="#4caf50", fg="white",
    command=add_water
)
add_btn.pack(pady=10)

# Initial draw
update_bar()

root.mainloop()
