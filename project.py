"""Ghost Chase: eat all dots while A* ghosts hunt you. Run: python ghost_chase.py"""
import heapq
import random
import tkinter as tk

N, CELL, TICK = 21, 28, 120
BG, WALL, DOT, PLAYER = "#0b111b", "#2b3a67", "#f2c14e", "#ffd23f"
GHOST_COLORS = ["#ff5d5d", "#ff9ff3", "#4bd1ff"]
DIRS = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0),
        "w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}


def make_maze(n):
    """Perfect maze (recursive backtracker) plus a few loops so ghosts can be dodged."""
    grid = [[1] * n for _ in range(n)]
    grid[1][1] = 0
    stack = [(1, 1)]
    while stack:
        x, y = stack[-1]
        opts = [(dx, dy) for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0))
                if 0 < x + 2 * dx < n - 1 and 0 < y + 2 * dy < n - 1
                and grid[y + 2 * dy][x + 2 * dx] == 1]
        if not opts:
            stack.pop()
            continue
        dx, dy = random.choice(opts)
        grid[y + dy][x + dx] = 0
        grid[y + 2 * dy][x + 2 * dx] = 0
        stack.append((x + 2 * dx, y + 2 * dy))
    extra = n
    for _ in range(n * 40):
        if extra == 0:
            break
        x, y = random.randint(1, n - 2), random.randint(1, n - 2)
        if grid[y][x] == 1:
            horiz = grid[y][x - 1] == 0 and grid[y][x + 1] == 0 and grid[y - 1][x] == 1 and grid[y + 1][x] == 1
            vert = grid[y - 1][x] == 0 and grid[y + 1][x] == 0 and grid[y][x - 1] == 1 and grid[y][x + 1] == 1
            if horiz or vert:
                grid[y][x] = 0
                extra -= 1
    return grid


def astar(grid, start, goal):
    """Shortest path from start to goal (inclusive), using Manhattan distance."""
    def h(p):
        return abs(p[0] - goal[0]) + abs(p[1] - goal[1])

    frontier = [(h(start), 0, start)]
    came, cost = {start: None}, {start: 0}
    while frontier:
        _, c, u = heapq.heappop(frontier)
        if u == goal:
            break
        if c > cost[u]:
            continue
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            v = (u[0] + dx, u[1] + dy)
            if grid[v[1]][v[0]] == 0 and c + 1 < cost.get(v, 1 << 30):
                cost[v] = c + 1
                came[v] = u
                heapq.heappush(frontier, (c + 1 + h(v), c + 1, v))
    if goal not in came:
        return []
    path, cur = [], goal
    while cur is not None:
        path.append(cur)
        cur = came[cur]
    return path[::-1]


class Game:
    def __init__(self, root):
        self.root = root
        root.title("Ghost Chase (A*)")
        root.configure(bg=BG)
        root.resizable(False, False)
        self.info = tk.Label(root, font=("Courier", 13, "bold"), bg=BG, fg="#e7ecf4")
        self.info.pack(pady=(10, 2))
        self.canvas = tk.Canvas(root, width=N * CELL, height=N * CELL, bg=BG, highlightthickness=0)
        self.canvas.pack(padx=14, pady=6)
        tk.Label(root, font=("Helvetica", 10), bg=BG, fg="#93a0b5",
                 text="Arrows / WASD move   P: show ghost A* paths   Space: pause   R: restart"
                 ).pack(pady=(0, 10))
        root.bind("<Key>", self.key)
        self.show_path = True
        self.restart()
        self.tick()

    # ----- state -----
    def restart(self):
        self.score, self.lives, self.level = 0, 3, 1
        self.over = self.paused = False
        self.new_level()

    def new_level(self):
        self.grid = make_maze(N)
        self.dots = {(x, y) for y in range(N) for x in range(N) if self.grid[y][x] == 0} - {(1, 1)}
        self.reset_positions(count=min(1 + self.level // 2, 3))

    def reset_positions(self, count=None):
        count = count or len(self.ghosts)
        corners = [(N - 2, N - 2), (N - 2, 1), (1, N - 2)]
        self.pl, self.dir, self.want = (1, 1), None, None
        self.ghosts = [{"pos": corners[i], "home": corners[i], "acc": 0.0, "path": []}
                       for i in range(count)]
        self.freeze = 8

    def ghost_speed(self):
        return min(0.5 + 0.06 * self.level, 0.9)

    # ----- input -----
    def key(self, e):
        k = e.keysym if e.keysym in DIRS else e.char
        if k in DIRS:
            self.want = DIRS[k]
        elif k in ("p", "P"):
            self.show_path = not self.show_path
        elif k == " ":
            self.paused = not self.paused
        elif k in ("r", "R"):
            self.restart()

    # ----- game loop -----
    def move_player(self):
        for d in (self.want, self.dir):
            if d is None:
                continue
            nx, ny = self.pl[0] + d[0], self.pl[1] + d[1]
            if self.grid[ny][nx] == 0:
                self.dir, self.pl = d, (nx, ny)
                return

    def caught(self):
        self.lives -= 1
        if self.lives <= 0:
            self.over = True
        else:
            self.reset_positions()

    def tick(self):
        if not self.over and not self.paused:
            if self.freeze > 0:
                self.freeze -= 1
            else:
                self.step()
        self.draw()
        self.root.after(TICK, self.tick)

    def step(self):
        self.move_player()
        if self.pl in self.dots:
            self.dots.discard(self.pl)
            self.score += 10
            if not self.dots:
                self.level += 1
                self.score += 100
                self.new_level()
                return
        if any(g["pos"] == self.pl for g in self.ghosts):
            return self.caught()
        for g in self.ghosts:
            g["acc"] += self.ghost_speed()
            while g["acc"] >= 1:
                g["acc"] -= 1
                g["path"] = astar(self.grid, g["pos"], self.pl)
                if len(g["path"]) > 1:
                    g["pos"] = g["path"][1]
                if g["pos"] == self.pl:
                    return self.caught()
            g["path"] = astar(self.grid, g["pos"], self.pl)

    # ----- drawing -----
    def draw(self):
        c, s = self.canvas, CELL
        c.delete("all")
        mid = lambda p: ((p[0] + .5) * s, (p[1] + .5) * s)
        for y in range(N):
            for x in range(N):
                if self.grid[y][x]:
                    c.create_rectangle(x * s, y * s, x * s + s, y * s + s, fill=WALL, outline=BG, width=2)
        for x, y in self.dots:
            c.create_oval(x * s + 11, y * s + 11, x * s + 17, y * s + 17, fill=DOT, outline="")
        for i, g in enumerate(self.ghosts):
            if self.show_path and len(g["path"]) > 1:
                pts = [v for p in g["path"] for v in mid(p)]
                c.create_line(*pts, fill=GHOST_COLORS[i], width=2, dash=(3, 4))
        for i, g in enumerate(self.ghosts):
            cx, cy = mid(g["pos"])
            c.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, fill=GHOST_COLORS[i], outline="")
            for ex in (-4, 4):
                c.create_oval(cx + ex - 3, cy - 5, cx + ex + 3, cy + 1, fill="white", outline="")
        cx, cy = mid(self.pl)
        c.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, fill=PLAYER, outline="")
        self.info.config(text="Score %d   Lives %s   Level %d" % (self.score, "♥" * self.lives, self.level))
        msg = "GAME OVER  (press R)" if self.over else ("PAUSED" if self.paused else None)
        if msg:
            c.create_rectangle(0, N * s // 2 - 28, N * s, N * s // 2 + 28, fill=BG, outline=WALL)
            c.create_text(N * s // 2, N * s // 2, text=msg, fill="#e7ecf4", font=("Helvetica", 20, "bold"))


if __name__ == "__main__":
    root = tk.Tk()
    Game(root)
    root.mainloop()
