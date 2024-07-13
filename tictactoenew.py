import sqlite3
from tkinter import *
from tabulate import tabulate
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.root = Tk()
        self.root.title("Tic Tac Toe")

        self.current_player = None
        self.player_X = None
        self.player_O = None
        self.board = [["" for i in range(3)] for i in range(3)]
        self.buttons = [[None for i in range(3)] for i in range(3)]

        self.conn = sqlite3.connect("tictactoe.db")
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS games 
                            (id INTEGER PRIMARY KEY, player_x TEXT, player_o TEXT, winner TEXT)''')

        self.create_login_window()

    def create_login_window(self):
        self.login_window = Toplevel(self.root)
        self.login_window.title("Player Login")

        Label(self.login_window, text="Player X").grid(row=0, column=0)
        self.player_X_entry = Entry(self.login_window)
        self.player_X_entry.grid(row=0, column=1)

        Label(self.login_window, text="Player O").grid(row=1, column=0)
        self.player_O_entry = Entry(self.login_window)
        self.player_O_entry.grid(row=1, column=1)

        Button(self.login_window, text="Start Game", command=self.start_game).grid(row=2, columnspan=2)

    def start_game(self):
        self.player_X = self.player_X_entry.get()
        self.player_O = self.player_O_entry.get()
        self.login_window.destroy()

        self.current_player = "X"
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = Button(self.root, text="", font=("Helvetica", 20), width=4, height=2,
                                            command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def make_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            if self.current_player == "X":
                self.buttons[row][col].config(text=self.current_player, fg='red')
            else:
                self.buttons[row][col].config(text=self.current_player, fg='blue')

            if self.check_winner(row, col):
                winner = self.player_X if self.current_player == "X" else self.player_O
                messagebox.showinfo("Winner", f"{winner} wins!")
                self.record_game_result(self.player_X, self.player_O, winner)
                self.display_game_results()
                self.reset_game()
            elif self.check_draw():
                messagebox.showinfo("Draw", "It's a draw!")
                self.record_game_result(self.player_X, self.player_O, "Draw")
                self.display_game_results()
                self.reset_game()
            else:
                if self.current_player == "X":
                    self.current_player = "O"
                else:
                    self.current_player = "X"

    def check_winner(self, row, col):
        # Check row
        if self.board[row][0] == self.board[row][1] == self.board[row][2] == self.current_player:
            return True
        # Check column
        if self.board[0][col] == self.board[1][col] == self.board[2][col] == self.current_player:
            return True
        # Check diagonals
        if (row == col and self.board[0][0] == self.board[1][1] == self.board[2][2] == self.current_player) or \
                (row + col == 2 and self.board[0][2] == self.board[1][1] == self.board[2][0] == self.current_player):
            return True
        return False

    def check_draw(self):
        for row in self.board:
            for cell in row:
                if cell == "":
                    return False
        return True

    def reset_game(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j] = ""
                self.buttons[i][j].config(text="")
        self.current_player = "X"

    def record_game_result(self, player_x, player_o, winner):
        self.cur.execute("INSERT INTO games (player_x, player_o, winner) VALUES (?, ?, ?)", (player_x, player_o, winner))
        self.conn.commit()

    def display_game_results(self):
        self.cur.execute("SELECT * FROM games")
        rows = self.cur.fetchall()
        headers = ["ID", "Player X", "Player O", "Winner"]
        print(tabulate(rows, headers=headers, tablefmt="grid"))

    def run(self):
        self.root.mainloop()

game = TicTacToe()
game.run()
