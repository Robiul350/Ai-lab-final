"""Tic-Tac-Toe vs Minimax AI (alpha-beta pruning). Run: python minimax_game.py"""
import random
import tkinter as tk

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

BG, PANEL, INK, MUTED = "#0d121b", "#141b27", "#e7ecf4", "#93a0b5"
X_COL, O_COL, WIN_COL = "#ff7a55", "#5b9bff", "#35c58d"


def winner(board):
    for a, b, c in LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], (a, b, c)
    return None, None


def minimax(board, turn, depth, alpha, beta):
    """AI is 'O' (maximizer), human is 'X' (minimizer)."""
    w, _ = winner(board)
    if w == "O":
        return 10 - depth
    if w == "X":
        return depth - 10
    if all(board):
        return 0
    if turn == "O":
        best = -99
        for i in range(9):
            if not board[i]:
                board[i] = "O"
                best = max(best, minimax(board, "X", depth + 1, alpha, beta))
                board[i] = None
                alpha = max(alpha, best)
                if alpha >= beta:
                    break
        return best
    best = 99
    for i in range(9):
        if not board[i]:
            board[i] = "X"
            best = min(best, minimax(board, "O", depth + 1, alpha, beta))
            board[i] = None
            beta = min(beta, best)
            if alpha >= beta:
                break
    return best


def best_move(board):
    scores = []
    for i in range(9):
        if not board[i]:
            board[i] = "O"
            scores.append((minimax(board, "X", 1, -99, 99), i))
            board[i] = None
    top = max(s for s, _ in scores)
    return random.choice([i for s, i in scores if s == top])


class Game:
    CELL = 120

    def __init__(self, root):
        self.root = root
        root.title("Minimax Tic-Tac-Toe")
        root.configure(bg=BG)
        root.resizable(False, False)
        self.score = {"You": 0, "Draw": 0, "AI": 0}
        self.hard = tk.BooleanVar(value=True)

        self.status = tk.Label(root, font=("Helvetica", 14, "bold"),
                               bg=BG, fg=INK)
        self.status.pack(pady=(14, 4))
        self.scoreboard = tk.Label(root, font=("Courier", 11), bg=BG, fg=MUTED)
        self.scoreboard.pack()

        size = self.CELL * 3
        self.canvas = tk.Canvas(root, width=size, height=size, bg=PANEL,
                                highlightthickness=0)
        self.canvas.pack(padx=20, pady=12)
        self.canvas.bind("<Button-1>", self.click)

        bar = tk.Frame(root, bg=BG)
        bar.pack(pady=(0, 14))
        tk.Button(bar, text="New game", command=self.new_game).pack(side="left", padx=6)
        tk.Checkbutton(bar, text="Hard (perfect AI)", variable=self.hard,
                       bg=BG, fg=INK, selectcolor=PANEL, activebackground=BG,
                       activeforeground=INK, command=self.new_game).pack(side="left", padx=6)
        self.new_game()

    def new_game(self):
        self.board = [None] * 9
        self.over = False
        self.line = None
        self.status.config(text="Your turn (X)")
        self.draw()

    def draw(self):
        c, s = self.canvas, self.CELL
        c.delete("all")
        for k in (1, 2):
            c.create_line(k * s, 12, k * s, 3 * s - 12, fill=MUTED, width=2)
            c.create_line(12, k * s, 3 * s - 12, k * s, fill=MUTED, width=2)
        for i, v in enumerate(self.board):
            x, y = (i % 3) * s, (i // 3) * s
            pad = 30
            col = WIN_COL if self.line and i in self.line else (X_COL if v == "X" else O_COL)
            if v == "X":
                c.create_line(x + pad, y + pad, x + s - pad, y + s - pad, fill=col, width=8, capstyle="round")
                c.create_line(x + s - pad, y + pad, x + pad, y + s - pad, fill=col, width=8, capstyle="round")
            elif v == "O":
                c.create_oval(x + pad, y + pad, x + s - pad, y + s - pad, outline=col, width=8)
        self.scoreboard.config(
            text="You %d   Draw %d   AI %d" % (self.score["You"], self.score["Draw"], self.score["AI"]))

    def click(self, event):
        if self.over:
            return
        i = (event.y // self.CELL) * 3 + (event.x // self.CELL)
        if not (0 <= i < 9) or self.board[i]:
            return
        self.board[i] = "X"
        if self.check():
            return
        self.status.config(text="AI is thinking...")
        self.root.after(350, self.ai_turn)

    def ai_turn(self):
        free = [i for i in range(9) if not self.board[i]]
        if not self.hard.get() and random.random() < 0.4:
            move = random.choice(free)
        else:
            move = best_move(self.board)
        self.board[move] = "O"
        if not self.check():
            self.status.config(text="Your turn (X)")

    def check(self):
        w, line = winner(self.board)
        if w:
            self.over, self.line = True, line
            who = "You" if w == "X" else "AI"
            self.score[who] += 1
            self.status.config(text="You win!" if w == "X" else "AI wins!")
        elif all(self.board):
            self.over = True
            self.score["Draw"] += 1
            self.status.config(text="Draw")
        self.draw()
        return self.over


if __name__ == "__main__":
    root = tk.Tk()
    Game(root)
    root.mainloop()