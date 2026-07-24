import pygame

CELL_SIZE = 40


class Renderer:
    def __init__(self, game_state, cell_size=CELL_SIZE):
        pygame.init()
        self.cell_size = cell_size
        self.cell_number = game_state.cell_number
        self.window = pygame.display.set_mode(
            (self.cell_number * cell_size, self.cell_number * cell_size)
        )
        pygame.display.set_caption("Learn2Slither")
        self.colors = {
            "background": (30, 30, 30),
            "grid": (45, 45, 45),
            "snake_head": (0, 140, 255),
            "snake_body": (0, 90, 200),
            "green_apple": (40, 200, 40),
            "red_apple": (210, 40, 40),
        }

    def draw(self, game_state):
        self.window.fill(self.colors["background"])
        self._draw_grid()
        self._draw_apples(game_state)
        self._draw_snake(game_state.snake)
        pygame.display.update()

    def _draw_grid(self):
        for x in range(self.cell_number):
            for y in range(self.cell_number):
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.window, self.colors["grid"], rect, 1)

    def _draw_apples(self, game_state):
        for apple in game_state.green_apples:
            self._draw_cell(apple.position, self.colors["green_apple"])
        self._draw_cell(game_state.red_apple.position, self.colors["red_apple"])

    def _draw_snake(self, snake):
        for i, block in enumerate(snake.body):
            color = self.colors["snake_head"] if i == 0 else self.colors["snake_body"]
            self._draw_cell(block, color)

    def _draw_cell(self, position, color):
        rect = pygame.Rect(
            int(position.x) * self.cell_size,
            int(position.y) * self.cell_size,
            self.cell_size,
            self.cell_size,
        )
        pygame.draw.rect(self.window, color, rect)

    def close(self):
        pygame.quit()
