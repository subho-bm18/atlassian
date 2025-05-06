import unittest
from snake_game import Cell, Snake

class TestCell(unittest.TestCase):
    def test_cell_equality(self):
        self.assertEqual(Cell(1, 2), Cell(1, 2))
        self.assertNotEqual(Cell(1, 2), Cell(2, 1))

class TestSnake(unittest.TestCase):
    def setUp(self):
        self.snake = Snake([Cell(1, 1), Cell(0, 1)])

    def test_initial_head(self):
        self.assertEqual(self.snake.head(), Cell(1, 1))

    def test_move_right(self):
        self.snake.direction = "RIGHT"
        self.snake.move()
        self.assertEqual(self.snake.head(), Cell(2, 1))
        self.assertEqual(len(self.snake.body), 2)  # should not grow

    def test_grow(self):
        self.snake.direction = "RIGHT"
        self.snake.grow()
        self.snake.move()
        self.assertEqual(len(self.snake.body), 3)

    def test_self_collision(self):
        self.snake.body = [Cell(2, 1), Cell(1, 1), Cell(1, 2), Cell(2, 2), Cell(2, 1)]  # circular
        self.assertTrue(self.snake.is_collision())

if __name__ == '__main__':
    unittest.main()
