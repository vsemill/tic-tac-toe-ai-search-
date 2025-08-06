import tkinter as tk
from tkinter import messagebox
import math
import time
import random

# --- Core Game Logic (from the previous version) ---

class TicTacToe:
    """Represents the Tic-Tac-Toe board and game logic."""
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.human_player = 'X'
        self.bot_player = 'O'

    def make_move(self, square, letter):
        """Places the player's letter on the board if the square is empty."""
        if self.board[square] == ' ':
            self.board[square] = letter
            return True
        return False

    def available_moves(self):
        """Returns a list of indices of empty squares."""
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def check_for_winner(self):
        """Checks the entire board for a winner."""
        # Check rows
        for i in range(3):
            if self.board[i*3] == self.board[i*3+1] == self.board[i*3+2] and self.board[i*3] != ' ':
                return self.board[i*3]
        # Check columns
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] and self.board[i] != ' ':
                return self.board[i]
        # Check diagonals
        if self.board[0] == self.board[4] == self.board[8] and self.board[0] != ' ':
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] and self.board[2] != ' ':
            return self.board[2]
        return None

def minimax(state, player):
    """The core logic for the bot's decision making."""
    max_player = state.bot_player
    other_player = state.human_player if player == state.bot_player else state.bot_player

    winner = state.check_for_winner()
    if winner:
        score = 1 * (len(state.available_moves()) + 1) if winner == max_player else -1 * (len(state.available_moves()) + 1)
        return {'position': None, 'score': score}
    
    if not state.available_moves():
        return {'position': None, 'score': 0}

    best = {'position': None, 'score': -math.inf if player == max_player else math.inf}
    
    for possible_move in state.available_moves():
        state.make_move(possible_move, player)
        sim_score = minimax(state, other_player)
        state.board[possible_move] = ' '
        sim_score['position'] = possible_move

        if player == max_player:
            if sim_score['score'] > best['score']:
                best = sim_score
        else:
            if sim_score['score'] < best['score']:
                best = sim_score
    return best

# --- GUI Class ---

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        master.title("Tic-Tac-Toe")
        master.configure(bg='#282c34') # Dark background color

        self.game = TicTacToe()
        self.buttons = []
        self.turn = None # To be set in start_game
        self.selected_index = 4 # For keyboard navigation

        # --- Styling ---
        self.button_font = ('Helvetica', 20, 'bold')
        self.status_font = ('Helvetica', 14)
        self.human_color = '#61dafb' # Blue for 'X'
        self.bot_color = '#ff7b72' # Red for 'O'
        self.bg_color = '#282c34'
        self.fg_color = '#ffffff'
        self.button_bg = '#444c56'
        self.highlight_bg = '#e5c07b' # Yellow/gold for highlight

        # --- Widgets ---
        self.status_label = tk.Label(master, text="Welcome to Tic-Tac-Toe!", font=self.status_font, bg=self.bg_color, fg=self.fg_color, pady=10)
        self.status_label.pack(fill=tk.X)

        board_frame = tk.Frame(master, bg=self.bg_color)
        board_frame.pack()

        for i in range(9):
            button = tk.Button(board_frame, text=' ', font=self.button_font, width=5, height=2,
                               bg=self.button_bg, fg=self.fg_color,
                               command=lambda i=i: self.handle_click(i))
            button.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(button)

        restart_button = tk.Button(master, text="Play Again", font=self.status_font, command=self.reset_game, bg='#61dafb', fg='#282c34')
        restart_button.pack(pady=20)

        # --- Keyboard Bindings ---
        self.master.bind('<Key>', self.handle_key_press)

        self.start_game()

    def start_game(self):
        """Starts a new game, randomly deciding the first turn."""
        if random.choice([0, 1]) == 0:
            self.turn = self.game.human_player
            self.status_label.config(text="You will go first.")
        else:
            self.turn = self.game.bot_player
            self.status_label.config(text="The bot will go first.")
            self.master.after(500, self.bot_turn)
        self.highlight_selection()

    def handle_key_press(self, event):
        """Handles keyboard input for board navigation and selection."""
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
        """Highlights the currently selected button."""
        is_player_turn = self.turn == self.game.human_player
        for i, button in enumerate(self.buttons):
            if button['state'] == 'normal':
                if i == self.selected_index and is_player_turn:
                    button.config(bg=self.highlight_bg)
                else:
                    button.config(bg=self.button_bg)

    def handle_click(self, index):
        """Handles a click on a board button by the human player."""
        if self.turn == self.game.human_player and self.game.board[index] == ' ':
            self.game.make_move(index, self.game.human_player)
            self.buttons[index].config(text=self.game.human_player, state='disabled', disabledforeground=self.human_color)
            
            if self.check_game_over():
                return
            
            self.turn = self.game.bot_player
            self.status_label.config(text="Bot's turn...")
            self.highlight_selection() # Clear highlight
            self.master.after(500, self.bot_turn)

    def bot_turn(self):
        """Handles the bot's turn."""
        if self.turn == self.game.bot_player:
            move_data = minimax(self.game, self.game.bot_player)
            bot_move_index = move_data['position']

            self.game.make_move(bot_move_index, self.game.bot_player)
            self.buttons[bot_move_index].config(text=self.game.bot_player, state='disabled', disabledforeground=self.bot_color)
            
            if self.check_game_over():
                return

            self.turn = self.game.human_player
            self.status_label.config(text="Your turn.")
            self.highlight_selection()

    def check_game_over(self):
        """Checks for a win or a tie and ends the game if necessary."""
        winner = self.game.check_for_winner()
        if winner:
            self.end_game(f"'{winner}' wins!")
            return True
        elif not self.game.available_moves():
            self.end_game("It's a tie!")
            return True
        return False

    def end_game(self, message):
        """Disables the board and shows the final message."""
        self.status_label.config(text=message)
        for button in self.buttons:
            button.config(state='disabled')
        self.highlight_selection() # Clear any remaining highlight
        messagebox.showinfo("Game Over", message)

    def reset_game(self):
        """Resets the game to its initial state for a new round."""
        self.game = TicTacToe()
        self.selected_index = 4
        for button in self.buttons:
            button.config(text=' ', state='normal')
        self.start_game()

# Main execution block
if __name__ == '__main__':
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()