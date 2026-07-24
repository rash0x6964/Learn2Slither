from environment.entities import Snake, GreenApple, RedApple


class GameState:
    def __init__(self, cell_number=10):
        self.cell_number = cell_number
        self.snake = Snake(cell_number)
        self.green_apples = []
        self.red_apple = None
        self.steps = 0
        self.max_length_reached = self.snake.length
        self._spawn_apples()

    def _forbidden_cells(self):
        cells = list(self.snake.body)
        cells += [a.position for a in self.green_apples]
        if self.red_apple is not None:
            cells.append(self.red_apple.position)
        return cells

    def _spawn_apples(self):
        self.green_apples = [
            GreenApple(self.cell_number, self._forbidden_cells()) for _ in range(2)
        ]
        self.red_apple = RedApple(self.cell_number, self._forbidden_cells())

    def reset(self):
        self.snake.reset()
        self.steps = 0
        self.max_length_reached = self.snake.length
        self._spawn_apples()

    def step(self, direction=None):
        self.snake.move(direction)
        self.steps += 1

        ate = None
        alive = True

        for apple in self.green_apples:
            if apple.position == self.snake.head:
                apple.apply(self.snake)
                apple.randomize(self._forbidden_cells())
                ate = "green"
                break

        if ate is None and self.red_apple.position == self.snake.head:
            alive = self.red_apple.apply(self.snake)
            self.red_apple.randomize(self._forbidden_cells())
            ate = "red"

        if alive and (self.snake.hit_wall() or self.snake.hit_self()):
            alive = False

        if alive and self.snake.length == 0:
            alive = False

        self.max_length_reached = max(self.max_length_reached, self.snake.length)

        return {
            "alive": alive,
            "ate": ate,
            "length": self.snake.length,
            "steps": self.steps,
            "max_length": self.max_length_reached,
        }
