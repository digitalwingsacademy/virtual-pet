import tkinter as tk
import time

CELL_SIZE = 60
ROWS = 10
COLS = 10

_pet = None

def move():
    _pet.move()

def turn_left():
    _pet.turn_left()

def put_ball():
    _pet.put_ball()

def front_is_blocked():
    return _pet.front_is_blocked()

class VirtualPet:
    def __init__(self, canvas):
        self.canvas = canvas
        self.row = ROWS - 1
        self.col = 0
        self.dir = 'E'
        self.balls = set()
        self.draw_world()

    def draw_world(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray")
        self.draw_balls()
        self.draw_pet()

    def draw_pet(self):
        x = self.col * CELL_SIZE + CELL_SIZE / 2
        y = self.row * CELL_SIZE + CELL_SIZE / 2
        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="brown")
        dx, dy = 0, 0
        if self.dir == 'N': dy = -15
        elif self.dir == 'S': dy = 15
        elif self.dir == 'E': dx = 15
        elif self.dir == 'W': dx = -15
        self.canvas.create_oval(x + dx - 5, y + dy - 5, x + dx + 5, y + dy + 5, fill="white")

    def draw_balls(self):
        for (r, c) in self.balls:
            x = c * CELL_SIZE + CELL_SIZE / 2
            y = r * CELL_SIZE + CELL_SIZE / 2
            self.canvas.create_oval(x - 7, y - 7, x + 7, y + 7, fill="orange")

    def move(self):
        if self.dir == 'N' and self.row > 0:
            self.row -= 1
        elif self.dir == 'S' and self.row < ROWS - 1:
            self.row += 1
        elif self.dir == 'E' and self.col < COLS - 1:
            self.col += 1
        elif self.dir == 'W' and self.col > 0:
            self.col -= 1
        self.draw_world()
        time.sleep(0.3)

    def turn_left(self):
        directions = ['N', 'W', 'S', 'E']
        idx = directions.index(self.dir)
        self.dir = directions[(idx + 1) % 4]
        self.draw_world()
        time.sleep(0.3)

    def put_ball(self):
        self.balls.add((self.row, self.col))
        self.draw_world()
        time.sleep(0.3)

    def front_is_blocked(self):
        if self.dir == 'N': return self.row == 0
        if self.dir == 'S': return self.row == ROWS - 1
        if self.dir == 'E': return self.col == COLS - 1
        if self.dir == 'W': return self.col == 0
        return True

def run(program):
    global _pet
    root = tk.Tk()
    root.title("Virtual Pet Simulator")
    canvas = tk.Canvas(root, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE)
    canvas.pack()
    _pet = VirtualPet(canvas)
    program()
    root.mainloop()
