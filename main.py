import tkinter as tk
from tkinter import messagebox
import generator
import time

class MinesweeperGUI:
    def __init__(self, master, rows, columns, bomb_count):
        self.master = master
        self.rows = rows
        self.columns = columns
        self.bomb_count = bomb_count

        self.tiles = [[None for _ in range(columns)] for _ in range(rows)]
        self.grid = generator.Grid(rows, columns, bomb_count)
        self.original_state = {}  # Initialize the original state dictionary

        self.create_widgets()

         # Initialize the start time to None and the elapsed time to 0
        self.start_time = None
        self.elapsed_time = 0
        self.game_state = "ongoing"
        self.timer_label = tk.Label(self.master, text="Time: 0")
        self.timer_label.grid(row=self.rows + 2, column=0, columnspan=self.columns, pady=5)

        # Bind the on_tile_click method to all buttons
        for row in range(self.rows):
            for col in range(self.columns):
                button = self.tiles[row][col]
                button.bind('<Button-1>', lambda event, r=row, c=col: self.on_tile_click(r, c, event))

        self.hide_button_clicked = False
        self.show_button_clicked = False

        # Create a Frame to hold the "Show Grid" button
        show_grid_frame = tk.Frame(self.master)
        show_grid_frame.grid(row=self.rows, column=0, columnspan=self.columns, pady=10)

        # Create the "Show Grid" button inside the frame
        show_grid_button = tk.Button(show_grid_frame, text="Show Grid", command=self.show_entire_grid)
        show_grid_button.pack()

        # Create a Frame to hold the "Reset Grid" and "Hide Grid" buttons
        control_frame = tk.Frame(self.master)
        control_frame.grid(row=self.rows + 1, column=0, columnspan=self.columns, pady=10)

        # Create the "Reset Grid" button inside the frame
        reset_button = tk.Button(control_frame, text="Reset Grid", command=self.reset_grid)
        reset_button.grid(row=0, column=0, padx=5)

        # Create the "Hide Grid" button inside the frame
        hide_button = tk.Button(control_frame, text="Hide Grid", command=self.hide_grid)
        hide_button.grid(row=0, column=1, padx=5)

        self.show_grid_button = show_grid_button
        self.hide_button = hide_button

    def update_timer(self):
        if self.start_time is not None and self.game_state == "ongoing":
            current_time = time.time()
            self.elapsed_time = int(current_time - self.start_time)
            self.timer_label.config(text=f"Time: {self.elapsed_time}", fg="black")
        self.master.after(1000, self.update_timer)  # Update the timer label every second (1000 ms)

    def check_winner(self):
        for row in range(self.rows):
            for col in range(self.columns):
                button = self.tiles[row][col]
                if button.cget('state') == 'normal':
                    value = self.grid.grid_value(row, col)
                    if isinstance(value, int):
                        return False
        return True

    def create_widgets(self):
        # Create buttons for each tile in the grid
        for row in range(self.rows):
            for col in range(self.columns):
                button = tk.Button(self.master, width=3, height=1)
                button.grid(row=row, column=col)
                self.tiles[row][col] = button

                # Bind left-click (Button-1) and right-click (Button-3) events to the button
                button.bind('<Button-1>', lambda event, r=row, c=col: self.on_tile_click(r, c, event))
                button.bind('<Button-3>', lambda event, r=row, c=col: self.on_tile_right_click(r, c, event))

        # Create a Frame to hold the "Show Grid" button
        show_grid_frame = tk.Frame(self.master)
        show_grid_frame.grid(row=self.rows, column=0, columnspan=self.columns, pady=10)

        # Create the "Show Grid" button inside the frame
        show_grid_button = tk.Button(show_grid_frame, text="Show Grid", command=self.show_entire_grid)
        show_grid_button.pack()

        # Create a Frame to hold the "Reset Grid" and "Hide Grid" buttons
        control_frame = tk.Frame(self.master)
        control_frame.grid(row=self.rows + 1, column=0, columnspan=self.columns, pady=10)

        # Create the "Reset Grid" button inside the frame
        reset_button = tk.Button(control_frame, text="Reset Grid", command=self.reset_grid)
        reset_button.grid(row=0, column=0, padx=5)

        # Create the "Hide Grid" button inside the frame
        hide_button = tk.Button(control_frame, text="Hide Grid", command=self.hide_grid)
        hide_button.grid(row=0, column=1, padx=5)

    def on_tile_right_click(self, row, col, event):
        # Handle right-click event here for flag placement
        button = self.tiles[row][col]

        if button.cget('state') == 'normal':
            # Place a flag on the tile
            button.config(text='F', state='disabled', relief=tk.RAISED)
        elif button.cget('text') == 'F':
            # Remove the flag from the tile
            button.config(text='', state='normal', relief=tk.RAISED)

    def on_tile_click(self, row, col, event):

        # Start the timer when the user clicks the first tile
        if self.start_time is None:
            self.start_time = time.time()
            self.update_timer()

        # Handle tile click event here
        # You can reveal the tile, check for bomb, add flag, etc.
        value = self.grid.grid_value(row, col)
        button = self.tiles[row][col]

        if event.num == 1:  # Left-click
            if button.cget('state') == 'disabled':
                return  # Avoid processing revealed tiles

            if value == 'b':
                # Game over: Reveal all bombs and show "You Lost!" message
                self.game_state = "over"
                self.timer_label.configure(fg="red")
                self.reveal_all_bombs()
                messagebox.showinfo("Game Over", "You Lost!")

            else:
                button.config(text=str(value), state='disabled', relief=tk.SUNKEN)
                if value == 0:
                    button.config(text='')
                    self.reveal_neighbors_dfs(row, col, set())

                # Check for win condition
                if self.check_winner():
                    self.game_state = "win"
                    self.timer_label.configure(fg="red")
                    messagebox.showinfo("Congratulations", "You Won!")

    def reveal_all_bombs(self):
        for row in range(self.rows):
            for col in range(self.columns):
                value = self.grid.grid_value(row, col)
                button = self.tiles[row][col]
                if value == 'b':
                    button.config(text='B', state='disabled', relief=tk.SUNKEN)
                elif value == 0:
                    button.config(text='', state='disabled', relief=tk.SUNKEN)
                else:
                    button.config(text=str(value), state='disabled', relief=tk.SUNKEN)

    def reveal_neighbors_dfs(self, row, col, visited):
        visited.add((row, col))
        button = self.tiles[row][col]
        value = self.grid.grid_value(row, col)

        if button.cget('state') != 'disabled':
            button.config(text=str(value), state='disabled', relief=tk.SUNKEN)
            if value == 0:
                button.config(text='')

        if value == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue

                    nr, nc = row + dr, col + dc
                    if (0 <= nr < self.rows and 0 <= nc < self.columns and
                            (nr, nc) not in visited):
                        self.reveal_neighbors_dfs(nr, nc, visited)
        else:
            visited.add((row, col))

    def show_entire_grid(self):

        self.start_time = None
        self.timer_label.config(text="You Cheated", fg = "red")

        if not self.show_button_clicked:
            # Store the original state of each tile before revealing the grid
            self.original_state = {}
            for row in range(self.rows):
                for col in range(self.columns):
                    button = self.tiles[row][col]
                    self.original_state[(row, col)] = {
                        "text": button.cget('text'),
                        "state": button.cget('state'),
                        "relief": button.cget('relief')
                    }

                    value = self.grid.grid_value(row, col)
                    if value == "b":
                        button.config(text='B', state='disabled', relief=tk.SUNKEN)
                    else:
                        if value > 0:
                            button.config(text=str(value))
                        else:
                            button.config(text='', state='disabled', relief=tk.SUNKEN)

            # Disable the show_grid button & enable hide grin
            self.show_grid_button.config(state='disabled')
            self.hide_button.config(state="active")

            # Set the show_button_clicked flag to True
            self.show_button_clicked = True
            self.hide_button_clicked = False


    def reset_grid(self):
        # Reset the grid to its initial state (with random bombs)
        self.grid = generator.Grid(self.rows, self.columns, self.bomb_count)

        # Reset the text and state of all buttons
        for row in range(self.rows):
            for col in range(self.columns):
                button = self.tiles[row][col]
                button.config(text='', state='normal', relief=tk.RAISED)

        # Reset the timer to 0 and set the game state back to "ongoing"
        self.start_time = None
        self.elapsed_time = 0
        self.game_state = "ongoing"
        self.timer_label.config(text="Time: 0", fg = "black")

        # Setting Hide & Show grid settings back to normal

        self.hide_button.config(state='active')
        self.show_grid_button.config(state='active')

        self.hide_button_clicked = False
        self.show_button_clicked = False


    def hide_grid(self):
        if not self.hide_button_clicked:
            # Restore the original state of each tile to hide the revealed grid
            for row in range(self.rows):
                for col in range(self.columns):
                    button = self.tiles[row][col]
                    original_state = self.original_state[(row, col)]
                    button.config(
                        text=original_state["text"],
                        state=original_state["state"],
                        relief=original_state["relief"]
                    )

            # Disable the hide_grid button
            self.hide_button.config(state='disabled')
            self.show_grid_button.config(state='active')

            # Set the hide_button_clicked flag to True
            self.hide_button_clicked = True
            self.show_button_clicked = False

if __name__ == "__main__":
    rows, columns, bomb_count = 8, 8, 10

    root = tk.Tk()
    root.title("Minesweeper")
    root.resizable(False, False)

    minesweeper_gui = MinesweeperGUI(root, rows, columns, bomb_count)
    root.mainloop()
