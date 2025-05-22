# simulator.py
import tkinter as tk
import time

CELL_SIZE = 50
ROWS = 10
COLS = 10

_pet = None
_speed = 0.8  # default delay in seconds


def set_speed(value):
    global _speed
    # Invertir el slider: derecha = más rápido
    _speed = 1.6 - float(value)

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
        # self.img = tk.PhotoImage(file="squirrel.png")
        self.row = 0
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
                color = "#f0f8ff" if (r + c) % 2 == 0 else "#e6f2ff"
                self.canvas.create_rectangle(x1, (ROWS - 1 - r) * CELL_SIZE, x2, (ROWS - r) * CELL_SIZE, fill=color, outline="#999")
        self.draw_balls()
        self.draw_pet()

    def draw_pet(self):
        self.draw_pet_at(self.col, self.row)

    def draw_pet_at(self, col, row):
        x = col * CELL_SIZE + CELL_SIZE / 2
        y = (ROWS - 1 - row) * CELL_SIZE + CELL_SIZE / 2
        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="brown", tags="pet")
        dx, dy = 0, 0
        if self.dir == 'N': dy = -15
        elif self.dir == 'S': dy = 15
        elif self.dir == 'E': dx = 15
        elif self.dir == 'W': dx = -15
        self.canvas.create_oval(x + dx - 5, y + dy - 5, x + dx + 5, y + dy + 5, fill="white", tags="pet")

    def draw_balls(self):
        for (r, c) in self.balls:
            x = c * CELL_SIZE + CELL_SIZE / 2
            y = (ROWS - 1 - r) * CELL_SIZE + CELL_SIZE / 2
            self.canvas.create_oval(x - 7, y - 7, x + 7, y + 7, fill="orange")

    def move(self):
        old_col, old_row = self.col, self.row
        if self.dir == 'N' and self.row > 0:
            self.row -= 1
        elif self.dir == 'S' and self.row < ROWS - 1:
            self.row += 1
        elif self.dir == 'E' and self.col < COLS - 1:
            self.col += 1
        elif self.dir == 'W' and self.col > 0:
            self.col -= 1

        steps = 10
        for i in range(steps):
            progress = (i + 1) / steps
            inter_col = old_col + (self.col - old_col) * progress
            inter_row = old_row + (self.row - old_row) * progress
            self.canvas.delete("pet")
            self.draw_balls()
            self.draw_pet_at(inter_col, inter_row)
            self.canvas.update()
            time.sleep(_speed / steps)
        self.draw_world()

    def turn_left(self):
        directions = ['N', 'W', 'S', 'E']
        idx = directions.index(self.dir)
        self.dir = directions[(idx + 1) % 4]
        self.draw_world()
        time.sleep(_speed)

    def put_ball(self):
        self.balls.add((self.row, self.col))
        self.draw_world()
        time.sleep(_speed)

    def front_is_blocked(self):
        if self.dir == 'N': return self.row == 0
        if self.dir == 'S': return self.row == ROWS - 1
        if self.dir == 'E': return self.col == COLS - 1
        if self.dir == 'W': return self.col == 0
        return True


def run(program, expected_position=None, expected_direction=None, expected_balls=None):
    global _pet
    root = tk.Tk()
    root.title("Virtual Pet Simulator")
    canvas = tk.Canvas(root, width=COLS * CELL_SIZE + 2, height=ROWS * CELL_SIZE + 2)
    canvas.pack()

    speed_slider = tk.Scale(root, from_=0.1, to=1.5, resolution=0.1,
                            orient=tk.HORIZONTAL, label="Speed (seconds per step)",
                            command=set_speed)
    speed_slider.set(_speed)
    speed_slider.pack()

    _pet = VirtualPet(canvas)

    def run_program():
        program()
        print("Program started with speed:", _speed)

        success = True
        if expected_position and (expected_position != (_pet.row, _pet.col)):
            success = False
        if expected_direction and (expected_direction != _pet.dir):
            success = False
        if expected_balls and (expected_balls != _pet.balls):
            success = False

        if success:
            result_text = "✅ Good job!"
            color = "green"
        else:
            issues = []
            if expected_position and (expected_position != (_pet.row, _pet.col)):
                issues.append("final position")
            if expected_direction and (expected_direction != _pet.dir):
                issues.append("final direction")
            if expected_balls and (expected_balls != _pet.balls):
                issues.append("ball placement")
            issue_text = ", ".join(issues)
            result_text = f"❌ Try again – check your {issue_text}."
            color = "red"
        color = "green" if success else "red"
        result_label = tk.Label(speed_slider, text=result_text, font=("Arial", 12), anchor="w", padx=10, fg=color)
        result_label.pack(side=tk.RIGHT)

    root.after(1000, run_program)

    # Show grid initially without executing program
    root.mainloop()
