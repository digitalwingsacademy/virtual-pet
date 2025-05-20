import tkinter as tk
import time
import threading
from PIL import Image, ImageTk

CELL_SIZE = 60
GRID_ROWS = 10
GRID_COLS = 10

DIRECTIONS = ['N', 'E', 'S', 'W']
DIR_DELTAS = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1)
}

class VirtualPet:
    def __init__(self, canvas):
        self.canvas = canvas
        self.row = GRID_ROWS - 1  # Empezar en la fila inferior
        self.col = 0
        self.dir = 'E'
        self.ball_grid = [[0]*GRID_COLS for _ in range(GRID_ROWS)]
        self.running = False

        # Cargar imagen de ardilla y crear versiones rotadas (más grande)
        original = Image.open("squirrel_icon.png").resize((50, 50))
        self.images = {
            'N': ImageTk.PhotoImage(original.rotate(90)),
            'E': ImageTk.PhotoImage(original),
            'S': ImageTk.PhotoImage(original.rotate(270)),
            'W': ImageTk.PhotoImage(original.rotate(180)),
        }

        self.draw_world()

    def draw_world(self):
        self.canvas.delete("all")
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray")
                if self.ball_grid[r][c] > 0:
                    self.canvas.create_oval(x1+20, y1+20, x2-20, y2-20, fill="orange")
        self.draw_pet()

    def draw_pet(self):
        x = self.col * CELL_SIZE + CELL_SIZE // 2
        y = self.row * CELL_SIZE + CELL_SIZE // 2
        self.canvas.create_image(x, y, image=self.images[self.dir])

    def move(self):
        dr, dc = DIR_DELTAS[self.dir]
        new_r = self.row + dr
        new_c = self.col + dc
        if 0 <= new_r < GRID_ROWS and 0 <= new_c < GRID_COLS:
            self.row = new_r
            self.col = new_c
        self.draw_world()

    def turnLeft(self):
        idx = (DIRECTIONS.index(self.dir) - 1) % 4
        self.dir = DIRECTIONS[idx]
        self.draw_world()

    def putBall(self):
        self.ball_grid[self.row][self.col] += 1
        self.draw_world()

    def takeBall(self):
        if self.ball_grid[self.row][self.col] > 0:
            self.ball_grid[self.row][self.col] -= 1
        self.draw_world()

    def run_commands(self, code):
        self.running = True

        def delay_call(func):
            def wrapped(*args, **kwargs):
                if self.running:
                    func(*args, **kwargs)
                    time.sleep(0.5)
            return wrapped

        def runner():
            globals_scope = {
                'move': delay_call(self.move),
                'turnLeft': delay_call(self.turnLeft),
                'putBall': delay_call(self.putBall),
                'takeBall': delay_call(self.takeBall),
            }
            try:
                exec(code, globals_scope)
            except Exception as e:
                print("Error:", e)

        threading.Thread(target=runner).start()

    def stop(self):
        self.running = False

    def reset(self):
        self.row = GRID_ROWS - 1  # Fila inferior
        self.col = 0
        self.dir = 'E'
        self.ball_grid = [[0]*GRID_COLS for _ in range(GRID_ROWS)]
        self.draw_world()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Pet Simulator")

        self.canvas = tk.Canvas(root, width=GRID_COLS*CELL_SIZE, height=GRID_ROWS*CELL_SIZE, bg="white")
        self.canvas.pack()

        self.pet = VirtualPet(self.canvas)

        # Crear una nueva ventana para el editor de código
        self.editor_window = tk.Toplevel(self.root)
        self.editor_window.title("Code Editor")
        self.text = tk.Text(self.editor_window, height=15, width=60)
        self.text.pack()

        self.run_button = tk.Button(self.editor_window, text="Run", command=self.run_code)
        self.run_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(self.editor_window, text="Stop", command=self.pet.stop)
        self.stop_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(self.editor_window, text="Reset", command=self.pet.reset)
        self.reset_button.pack(side=tk.LEFT)

    def run_code(self):
        code = self.text.get("1.0", tk.END)
        self.pet.run_commands(code)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
