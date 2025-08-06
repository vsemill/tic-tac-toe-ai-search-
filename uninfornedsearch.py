import tkinter as tk
from tkinter import messagebox
import random

# --- Core Game Logic ---

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.human_player = 'X'
        self.bot_player = 'O'

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            return True
        return False

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def check_for_winner(self):
        # Check rows, columns, and diagonals for a winner
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # columns
            [0, 4, 8], [2, 4, 6] # diagonals
        ]
        for line in lines:
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]] and self.board[line[0]] != ' ':
                return self.board[line[0]]
        return None

# --- DFS Uninformed Search Implementation ---

def dfs_find_move(game_state):
    """
    Finds a move using Depth-First Search.
    It explores paths to find one that results in a win.
    If no winning path is found, it returns a random move.
    """
    bot_player = game_state.bot_player
    
    # Iterate through all possible first moves
    for move in game_state.available_moves():
        # Create a copy of the board to simulate the move
        temp_board = game_state.board.copy()
        temp_game = TicTacToe()
        temp_game.board = temp_board
        temp_game.make_move(move, bot_player)
        
        # Call the recursive DFS helper
        if dfs_recursive_check(temp_game, bot_player):
            # If the recursive check finds a winning path starting with this move, take it.
            return move
            
    # If no winning path is found after checking all initial moves, make a random move.
    return random.choice(game_state.available_moves())

def dfs_recursive_check(game_state, player_to_win):
    """
    A recursive helper for DFS. It explores the game tree from the given state.
    Returns True if a winning path is found for the 'player_to_win'.
    """
    # Base Case 1: If the current state is a win for the target player, a winning path is found.
    if game_state.check_for_winner() == player_to_win:
        return True
    
    # Base Case 2: If the board is full or the opponent won, this path is not a solution.
    if not game_state.available_moves() or game_state.check_for_winner() is not None:
        return False

    # Recursive Step: Explore deeper for each available move.
    # Note: A true DFS would only need to find one winning path, not necessarily explore all.
    # This simplified version checks if ANY of the subsequent paths lead to a win.
    for move in game_state.available_moves():
        temp_board = game_state.board.copy()
        temp_game = TicTacToe()
        temp_game.board = temp_board
        
        # Assume the game alternates turns. This is a simplification.
        # A full game simulation would be more complex.
        # For this example, we just check if any future state can lead to a win.
        temp_game.make_move(move, player_to_win)
        if dfs_recursive_check(temp_game, player_to_win):
            return True
            
    return False

# --- GUI Class ---

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        master.title("Tic-Tac-Toe (DFS Uninformed)")
        master.configure(bg='#282c34')

        self.game = TicTacToe()
        self.buttons = []
        self.turn = None
        self.selected_index = 4

        # Styling
        self.button_font = ('Helvetica', 20, 'bold')
        self.status_font = ('Helvetica', 14)
        self.human_color = '#61dafb'
        self.bot_color = '#ff7b72'
        self.bg_color = '#282c34'
        self.fg_color = '#ffffff'
        self.button_bg = '#444c56'
        self.highlight_bg = '#e5c07b'

        # Widgets
        self.status_label = tk.Label(master, text="Welcome to Tic-Tac-Toe!", font=self.status_font,
                                     bg=self.bg_color, fg=self.fg_color, pady=10)
        self.status_label.pack(fill=tk.X)

        board_frame = tk.Frame(master, bg=self.bg_color)
        board_frame.pack()

        for i in range(9):
            button = tk.Button(board_frame, text=' ', font=self.button_font, width=5, height=2,
                               bg=self.button_bg, fg=self.fg_color,
                               command=lambda i=i: self.handle_click(i))
            button.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(button)

        restart_button = tk.Button(master, text="Play Again", font=self.status_font, command=self.reset_game,
                                   bg='#61dafb', fg='#282c34')
        restart_button.pack(pady=20)

        self.master.bind('<Key>', self.handle_key_press)
        self.start_game()

    def start_game(self):
        if random.choice([0, 1]) == 0:
            self.turn = self.game.human_player
            self.status_label.config(text="You will go first.")
        else:
            self.turn = self.game.bot_player
            self.status_label.config(text="The bot will go first.")
            self.master.after(500, self.bot_turn)
        self.highlight_selection()

    def handle_key_press(self, event):
        if self.turn != self.game.human_player:
            return
        key = event.keysym
        current_index = self.selected_index
        if key == 'Up' and self.selected_index >= 3:
            self.selected_index -= 3
        elif key == 'Down' and self.selected_index < 6:
            self.selected_index += 3
        elif key == 'Left' and self.selected_index % 3 != 0:
            self.selected_index -= 1
        elif key == 'Right' and self.selected_index % 3 != 2:
            self.selected_index += 1
        elif key in ['Return', 'space']:
            if self.buttons[self.selected_index]['state'] == 'normal':
                self.handle_click(self.selected_index)

        if current_index != self.selected_index:
            self.highlight_selection()

    def highlight_selection(self):
        is_player_turn = self.turn == self.game.human_player
        for i, button in enumerate(self.buttons):
            if button['state'] == 'normal':
                if i == self.selected_index and is_player_turn:
                    button.config(bg=self.highlight_bg)
                else:
                    button.config(bg=self.button_bg)

    def handle_click(self, index):
        if self.turn == self.game.human_player and self.game.board[index] == ' ':
            self.game.make_move(index, self.game.human_player)
            self.buttons[index].config(text=self.game.human_player, state='disabled', disabledforeground=self.human_color)
            if self.check_game_over():
                return
            self.turn = self.game.bot_player
            self.status_label.config(text="Bot's turn...")
            self.highlight_selection()
            self.master.after(500, self.bot_turn)

    def bot_turn(self):
        if self.turn == self.game.bot_player and self.game.available_moves():
            # Call the DFS function to get the bot's move
            move = dfs_find_move(self.game)
            self.game.make_move(move, self.game.bot_player)
            self.buttons[move].config(text=self.game.bot_player, state='disabled', disabledforeground=self.bot_color)
            if self.check_game_over():
                return
            self.turn = self.game.human_player
            self.status_label.config(text="Your turn.")
            self.highlight_selection()

    def check_game_over(self):
        winner = self.game.check_for_winner()
        if winner:
            self.end_game(f"'{winner}' wins!")
            return True
        elif not self.game.available_moves():
            self.end_game("It's a tie!")
            return True
        return False

    def end_game(self, message):
        self.status_label.config(text=message)
        for button in self.buttons:
            button.config(state='disabled')
        self.highlight_selection()
        messagebox.showinfo("Game Over", message)

    def reset_game(self):
        self.game = TicTacToe()
        self.selected_index = 4
        for button in self.buttons:
            button.config(text=' ', state='normal')
        self.start_game()

# --- Run App ---
if __name__ == '__main__':
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()