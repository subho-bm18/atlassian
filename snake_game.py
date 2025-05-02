import random
from tkinter import *

# ---- Cell Class ----
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

# ---- Snake Class ----
class Snake:
    def __init__(self, initial_cells):
        self.body = initial_cells
        self.direction = "RIGHT"
        self.grow_on_next_move = False

    def move(self):
        head = self.body[0]
        if self.direction == "UP":
            new_head = Cell(head.x, head.y - 1)
        elif self.direction == "DOWN":
            new_head = Cell(head.x, head.y + 1)
        elif self.direction == "LEFT":
            new_head = Cell(head.x - 1, head.y)
        else:
            new_head = Cell(head.x + 1, head.y)

        self.body.insert(0, new_head)
        if not self.grow_on_next_move:
            self.body.pop()
        else:
            self.grow_on_next_move = False

    def grow(self):
        self.grow_on_next_move = True

    def head(self):
        return self.body[0]

    def is_collision(self):
        return self.head() in self.body[1:]

# ---- Board Class ----
class Board:
    def __init__(self, canvas, width, height, cell_size):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.food = None

    def place_food(self, occupied_cells):
        while True:
            x = random.randint(0, (self.width // self.cell_size) - 1)
            y = random.randint(0, (self.height // self.cell_size) - 1)
            food = Cell(x, y)
            if food not in occupied_cells:
                self.food = food
                break

    def draw(self, snake):
        self.canvas.delete("all")
        for segment in snake.body:
            self.draw_cell(segment, fill="#00FF00")
        if self.food:
            self.draw_cell(self.food, fill="#FF0000")

    def draw_cell(self, cell, fill):
        x1 = cell.x * self.cell_size
        y1 = cell.y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill)

# ---- Game Class ----
class Game:
    def __init__(self, window):
        self.window = window
        self.canvas = Canvas(window, width=700, height=700, bg="black")
        self.canvas.pack()

        self.board = Board(self.canvas, 700, 700, 25)
        initial_cells = [Cell(5, 5), Cell(4, 5), Cell(3, 5)]
        self.snake = Snake(initial_cells)
        self.board.place_food(self.snake.body)

        self.window.bind("<Key>", self.change_direction)
        self.game_loop()

    def change_direction(self, event):
        key = event.keysym
        if key == "Up" and self.snake.direction != "DOWN":
            self.snake.direction = "UP"
        elif key == "Down" and self.snake.direction != "UP":
            self.snake.direction = "DOWN"
        elif key == "Left" and self.snake.direction != "RIGHT":
            self.snake.direction = "LEFT"
        elif key == "Right" and self.snake.direction != "LEFT":
            self.snake.direction = "RIGHT"

    def game_loop(self):
        self.snake.move()

        if self.snake.head() == self.board.food:
            self.snake.grow()
            self.board.place_food(self.snake.body)

        if self.snake.is_collision() or not self.is_in_bounds(self.snake.head()):
            self.game_over()
            return

        self.board.draw(self.snake)
        self.window.after(150, self.game_loop)

    def is_in_bounds(self, cell):
        return 0 <= cell.x < (self.board.width // self.board.cell_size) and \
               0 <= cell.y < (self.board.height // self.board.cell_size)

    def game_over(self):
        self.canvas.create_text(350, 350, text="GAME OVER", font=('Consolas', 40), fill="red")

# ---- Main Program ----
if __name__ == '__main__':
    root = Tk()
    root.title("Snake Game OOP")
    game = Game(root)
    root.mainloop()
