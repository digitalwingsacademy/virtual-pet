# 🐾 Virtual Pet Simulator

An educational tool to learn Python programming through a virtual pet in a grid-based world.

---

## 🚀 Features

- 2D grid world (default size: 10x10).
- A virtual pet (default: a squirrel) that can:
  - Move forward with `move()`
  - Turn left with `turnLeft()`
  - Place a ball with `putBall()`
  - Pick up a ball with `takeBall()`
- Interactive graphical interface built with `tkinter`.
- Animated execution with visual delay between commands.
- Supports:
  - User-defined functions
  - Control structures: `if`, `else`, `for`, `while`, etc.
- Control buttons:
  - **Run** to execute student code
  - **Stop** to interrupt execution
  - **Reset** to reset the pet and the world

---

## 📦 Requirements

- Python 3.7+
- Libraries:
  - `tkinter` (usually included with Python)
  - `pillow` (for image support)

To install dependencies on **Ubuntu/Debian**:

```bash
sudo apt install python3-tk
pip install pillow
