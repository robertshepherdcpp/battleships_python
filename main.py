import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
import tkinter.messagebox as messagebox
import random

# Global variables
grid = [['.' for _ in range(10)] for _ in range(10)]
grid_size = 10
num_of_ships = 5
game_over = False
num_of_ships_sunk = 0
total_ship_part = 0
total_ship_pieces_sunk = 0

def is_valid_ship_position_col(random_col_start, random_col_end, random_row_for_cols):
    global grid
    is_all_fine = True
    for x in range(random_col_start, random_col_end + 1):
        if grid[random_row_for_cols][x] == 'O':
            is_all_fine = False
    return is_all_fine

def add_ship_to_grid_col(random_col_start, random_col_end, random_row_for_cols):
    global grid
    for x in range(random_col_start, random_col_end + 1):
        grid[random_row_for_cols][x] = 'O'

def generate_ship():
    global num_of_ships
    global total_ship_part

    direction_of_ship = 0
    if direction_of_ship == 0:
        random_row_for_cols = random.randint(0, 9)
        random_col_start = random.randint(0, 8)
        random_col_end = random.randint(random_col_start, 9)
        if is_valid_ship_position_col(random_col_start, random_col_end, random_row_for_cols):
            add_ship_to_grid_col(random_col_start, random_col_end, random_row_for_cols)
        else:
            while not is_valid_ship_position_col(random_col_start, random_col_end, random_row_for_cols):
                direction_of_ship = random.randint(0, 1)
                random_col_start = random.randint(0, 8)
                random_col_end = random.randint(random_col_start, 9)
            total_ship_part = total_ship_part + random_col_end - random_col_start
            add_ship_to_grid_col(random_col_start, random_col_end, random_row_for_cols)

class UserButtonGrid:
    def __init__(self, master):
        self.bullets_left = 50
        self.master = master
        self.buttons = []
        for i in range(10):
            row = []
            for j in range(10):
                button = tk.Button(master, width=2, height=1)
                button.grid(row=i, column=j)
                button.bind("<Button-1>", lambda event, i=i, j=j: self.button_clicked(event, i, j))
                button.bind("<Enter>", lambda event, i=i, j=j: self.highlighted(event, i, j))
                button.bind("<Leave>", lambda event, i=i, j=j: self.unhighlighted(event, i, j))
                button.config(bg="white")
                row.append(button)
            self.buttons.append(row)

    def button_clicked(self, event, i, j):
        global grid
        global total_ship_pieces_sunk
        global num_of_ships_sunk

        if not game_over and self.bullets_left > 0:
            if grid[i][j] == 'O':
                self.buttons[i][j].configure(text="✅", bg="green")
                total_ship_pieces_sunk += 1
                if total_ship_pieces_sunk == total_ship_part:
                    self.show_game_over_message("Congratulations! You sunk all the ships!")
                if self.bullets_left <= 0:
                    self.show_game_over_message("You wasted all of your bullets before you sunk all the enemy ships!")
            else:
                self.buttons[i][j].configure(text="❌", bg="red")
            self.bullets_left -= 1

    def highlighted(self, event, i, j):
        if not game_over:
            self.buttons[i][j].config(bg="yellow")

    def unhighlighted(self, event, i, j):
        if not game_over:
            self.buttons[i][j].config(bg="white")

    def show_game_over_message(self, message):
        global game_over
        game_over = True
        for i in range(10):
            for j in range(10):
                self.buttons[i][j].unbind("<Button-1>")
        messagebox.showinfo("Game Over", message)

def restart_game():
    global game_over
    global grid
    global num_of_ships_sunk
    global total_ship_part
    global total_ship_pieces_sunk

    grid = [['.' for _ in range(10)] for _ in range(10)]
    game_over = False
    num_of_ships_sunk = 0
    total_ship_part = 0
    total_ship_pieces_sunk = 0

    for i in range(num_of_ships):
        generate_ship()

    for i in range(10):
        for j in range(10):
            user_grid.buttons[i][j].config(text="", bg="white")
            user_grid.buttons[i][j].bind("<Button-1>", lambda event, i=i, j=j: user_grid.button_clicked(event, i, j))
            user_grid.buttons[i][j].bind("<Enter>", lambda event, i=i, j=j: user_grid.highlighted(event, i, j))
            user_grid.buttons[i][j].bind("<Leave>", lambda event, i=i, j=j: user_grid.unhighlighted(event, i, j))

    user_grid.bullets_left = 50

root = tk.Tk()
root.title("Battleship Game")

for i in range(num_of_ships):
    generate_ship()

user_grid = UserButtonGrid(root)

restart_button = tk.Button(root, text="Restart", command=restart_game)
restart_button.grid(row=10, column=0, columnspan=10)

TitleFontObj = tkFont.Font(size=28)
l = Label(root, text="Battleships Game",
          width=40, height=5, font=TitleFontObj)

InstructionFontObj = tkFont.Font(size=14)
y = Label(root, text="If ✅ shows that means you have hit a ship, but if ❌ it means you have just hit water", width=80, height=10, font=InstructionFontObj)

root.mainloop()
